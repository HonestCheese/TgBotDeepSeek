import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import json
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class TaskDatabase:
    def __init__(self):
        """Подключаемся к PostgreSQL"""
        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        self.conn.autocommit = False
        self.create_tables()

    def create_tables(self):
        """Создаем таблицы, если их нет"""
        with self.conn.cursor() as cur:
            # Таблица задач
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    task_text TEXT NOT NULL,
                    deadline TIMESTAMP,
                    priority INTEGER DEFAULT 2, -- 1 самый важный, 2 стоит начать выполнение, 3 - еще можно потерпеть
                    status INTEGER DEFAULT 1,  -- 1 = не сделано, 0 = в процессе, -1 = выполнено
                    progress_context TEXT,     -- строка для хранения прогресса и контекста
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                );
            """)
            print("✅ Таблица tasks создана")

            # Индексы для задач
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_user 
                ON tasks(user_id, status)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_deadline 
                ON tasks(deadline) WHERE status = '1' OR status = '0'
            """)

            # Таблица контекста пользователя (важные факты, предпочтения)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_context (
                    user_id BIGINT PRIMARY KEY,
                    last_topics TEXT,  -- последние темы (JSON)
                    important_facts TEXT,  -- важные факты о пользователе
                    preferences TEXT,  -- предпочтения
                    productivity_pattern TEXT,  -- паттерны продуктивности
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Таблица истории диалогов
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    role VARCHAR(10),  -- 'user' или 'assistant'
                    message TEXT NOT NULL,
                    topic VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Индекс для быстрого поиска истории по пользователю
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_chat_user 
                ON chat_history(user_id, created_at)
            """)

            self.conn.commit()
            print("✅ PostgreSQL таблицы готовы")

    # ========== МЕТОДЫ ДЛЯ РАБОТЫ С ЗАДАЧАМИ ==========
    def add_task(self, user_id, task_text, deadline=None, priority=2):
        """
        Добавляет новую задачу в БД
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO tasks 
                    (user_id, task_text, deadline, priority, status, created_at)
                    VALUES (%s, %s, %s, %s, 1, CURRENT_TIMESTAMP)
                    RETURNING id;
                """, (user_id, task_text, deadline, priority))

                task_id = cur.fetchone()[0]
                self.conn.commit()

                print(f"✅ Задача #{task_id} добавлена для пользователя {user_id}")
                return task_id

        except Exception as e:
            print(f"❌ Ошибка при добавлении задачи: {e}")
            self.conn.rollback()
            return None

    def get_user_tasks(self, user_id):
        """
        Получает все задачи пользователя

        Args:
            user_id: ID пользователя в Telegram

        Returns:
            Список словарей с задачами пользователя
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        id,
                        user_id,
                        task_text,
                        deadline,
                        priority,
                        status,
                        progress_context,
                        created_at,
                        completed_at
                    FROM tasks 
                    WHERE user_id = %s 
                    ORDER BY 
                        priority ASC,  -- 1 (высокий) будет первым
                        created_at DESC;
                """, (user_id,))

                rows = cur.fetchall()

                # Преобразуем строки в словари
                tasks = []
                for row in rows:
                    task = {
                        'id': row[0],
                        'user_id': row[1],
                        'task_text': row[2],
                        'deadline': row[3],
                        'priority': row[4],  # 1, 2, 3
                        'status': row[5],  # 1 не сделано, 0 в процессе, -1 выполнено
                        'progress_context': row[6],
                        'created_at': row[7],
                        'completed_at': row[8]
                    }
                    tasks.append(task)

                print(f"📋 Получено {len(tasks)} задач для пользователя {user_id}")
                return tasks

        except Exception as e:
            print(f"❌ Ошибка при получении задач: {e}")
            return []  # Возвращаем пустой список в случае ошибки

    def complete_task(self, user_id, task_id=None, task_text=None):
        """
        Отмечает задачу как выполненную

        Args:
            user_id: ID пользователя
            task_id: ID задачи (если известен)
            task_text: текст задачи (поиск по тексту)

        Returns:
            True если успешно, False если задача не найдена
        """
        try:
            with self.conn.cursor() as cur:
                if task_id:
                    cur.execute("""
                        UPDATE tasks 
                        SET status = -1, completed_at = CURRENT_TIMESTAMP
                        WHERE id = %s AND user_id = %s AND status != -1
                        RETURNING id;
                    """, (task_id, user_id))
                elif task_text:
                    cur.execute("""
                        UPDATE tasks 
                        SET status = -1, completed_at = CURRENT_TIMESTAMP
                        WHERE user_id = %s AND task_text ILIKE %s AND status != -1
                        RETURNING id;
                    """, (user_id, f'%{task_text}%'))
                else:
                    return False

                result = cur.fetchone()
                self.conn.commit()

                if result:
                    print(f"✅ Задача #{result[0]} выполнена")
                    return True
                return False
        except Exception as e:
            print(f"❌ Ошибка при выполнении задачи: {e}")
            self.conn.rollback()
            return False

    def delete_task(self, user_id, task_id=None, task_text=None):
        """
        Удаляет задачу из БД

        Args:
            user_id: ID пользователя
            task_id: ID задачи (если известен)
            task_text: текст задачи (поиск по тексту)

        Returns:
            True если успешно, False если задача не найдена
        """
        try:
            with self.conn.cursor() as cur:
                if task_id:
                    cur.execute("""
                        DELETE FROM tasks 
                        WHERE id = %s AND user_id = %s
                        RETURNING id;
                    """, (task_id, user_id))
                elif task_text:
                    cur.execute("""
                        DELETE FROM tasks 
                        WHERE user_id = %s AND task_text ILIKE %s
                        RETURNING id;
                    """, (user_id, f'%{task_text}%'))
                else:
                    return False

                result = cur.fetchone()
                self.conn.commit()

                if result:
                    print(f"✅ Задача #{result[0]} удалена")
                    return True
                return False

        except Exception as e:
            print(f"❌ Ошибка при удалении задачи: {e}")
            self.conn.rollback()
            return False

    def update_task(self, user_id, task_id=None, task_text=None, new_task=None):
        """
        Обновляет задачу - записывает все поля которые пришли (включая task_text)
        """
        if not new_task:
            return False

        try:
            with self.conn.cursor() as cur:
                # Находим ID задачи
                if task_id:
                    cur.execute("SELECT id FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
                elif task_text:
                    cur.execute("SELECT id FROM tasks WHERE user_id = %s AND task_text ILIKE %s",
                                (user_id, f'%{task_text}%'))
                else:
                    return False

                result = cur.fetchone()
                if not result:
                    return False

                found_id = result[0]

                # ОБНОВЛЯЕМ ВСЕ ПОЛЯ КОТОРЫЕ ПРИШЛИ (ВКЛЮЧАЯ task_text)
                if 'task_text' in new_task:
                    cur.execute("UPDATE tasks SET task_text = %s WHERE id = %s",
                                (new_task['task_text'], found_id))

                if 'priority' in new_task:
                    cur.execute("UPDATE tasks SET priority = %s WHERE id = %s",
                                (new_task['priority'], found_id))

                if 'deadline' in new_task:
                    cur.execute("UPDATE tasks SET deadline = %s WHERE id = %s",
                                (new_task['deadline'], found_id))

                if 'status' in new_task:
                    cur.execute("UPDATE tasks SET status = %s WHERE id = %s",
                                (new_task['status'], found_id))

                if 'progress_context' in new_task:
                    cur.execute("UPDATE tasks SET progress_context = %s WHERE id = %s",
                                (new_task['progress_context'], found_id))

                if 'completed_at' in new_task:
                    cur.execute("UPDATE tasks SET completed_at = %s WHERE id = %s",
                                (new_task['completed_at'], found_id))

                self.conn.commit()
                print(f"🔄 Задача #{found_id} обновлена. Поля: {list(new_task.keys())}")
                return True

        except Exception as e:
            print(f"❌ Ошибка при обновлении задачи: {e}")
            self.conn.rollback()
            return False
        except Exception as e:
            print(f"❌ Ошибка при обновлении задачи: {e}")
            self.conn.rollback()
            return False

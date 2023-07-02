from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import *

def log_processing():

    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(env_settings)
    t_env.get_config().set("pipeline.jars", "file:///Users/Raghav/Desktop/DaftPunk/Resources/flink-sql-connector-kafka-1.17.1.jar;file:///Users/Raghav/Desktop/DaftPunk/Resources/mysql-connector-j-8.0.32.jar;file:///Users/Raghav/Desktop/DaftPunk/Resources/flink-connector-jdbc-3.1.0-1.17.jar")
    # t_env.get_config().set("pipeline.jars", "file:///Users/karanbawejapro/Desktop/jarfiles/flink-sql-connector-kafka-1.17.1.jar")
    t_env.get_config().set("table.exec.source.idle-timeout", "1000")
    # t_env.get_config().set("table.exec.non-temporal-sort.enabled", True)
    
    # Cursor Source 
    source_ddl_2 = """
        CREATE TABLE cursor_positions(
            sessionId VARCHAR,
            x INT,
            y INT,
            timestamp_cursor BIGINT,
            timez_ltz AS TO_TIMESTAMP_LTZ(timestamp_cursor,3),
            WATERMARK FOR timez_ltz AS timez_ltz - INTERVAL '5' SECONDS
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'cursor_positions',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'cursor_group',
            'scan.startup.mode' = 'specific-offsets',
            'scan.startup.specific-offsets' = 'partition:0,offset:0',
            'json.fail-on-missing-field' = 'false',
            'json.ignore-parse-errors' = 'true',
            'format' = 'json'
        )
        """  
    t_env.execute_sql(source_ddl_2)
    tbl_cursor = t_env.from_path('cursor_positions')
    tbl_cursor.print_schema()
    # tbl_cursor.execute().print()

    vel_query = """SELECT *,
                    CASE
                        WHEN t_delta IS NULL THEN 0
                        WHEN t_delta = 0 THEN 0
                        ElSE d_delta/t_delta
                    END AS speed
                FROM(
                    SELECT *, 
                    SQRT(POWER(diff_x,2) + POWER(diff_y,2)) AS d_delta 
                    FROM
                        (SELECT
                                sessionId,
                                x - LAG(x) OVER (PARTITION BY sessionId ORDER BY timez_ltz) AS diff_x,
                                y - LAG(y) OVER (PARTITION BY sessionId ORDER BY timez_ltz) AS diff_y,
                                timestamp_cursor - LAG(timestamp_cursor) OVER (PARTITION BY sessionId ORDER BY timez_ltz) AS t_delta
                            FROM
                                cursor_positions));
                """
    table_vel = t_env.sql_query(vel_query)
    t_env.register_table("table_vel", table_vel)

    sinka_kafka_cursor = """
            CREATE TABLE sink_kafka_cursor(
            sessionId VARCHAR,
            avg_vel DECIMAL(10,2),
            tot_dist DECIMAL(10,2),
            PRIMARY KEY (sessionId) NOT ENFORCED
            )WITH (
                'connector' = 'upsert-kafka',
                'topic' = 'feature_cursor',
                'properties.bootstrap.servers' = 'localhost:9092',
                'key.format' = 'json',
                'value.format' = 'json'
            );
    """
    t_env.execute_sql(sinka_kafka_cursor)

    computed_cursors = """
            INSERT INTO sink_kafka_cursor
            SELECT sessionId,
            AVG(speed) AS avg_vel,
            SUM(d_delta) AS tot_dist
            FROM table_vel
            GROUP BY sessionId;
    """
    t_env.execute_sql(computed_cursors).wait()



if __name__ == "__main__":
    log_processing()
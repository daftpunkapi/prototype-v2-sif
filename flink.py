from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import *
from pyflink.table.window import Tumble

def log_processing():

    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(env_settings)
    t_env.get_config().set("pipeline.jars", "file:///Users/Raghav/Desktop/DaftPunk/Resources/flink-sql-connector-kafka-1.17.1.jar;file:///Users/Raghav/Desktop/DaftPunk/Resources/mysql-connector-j-8.0.32.jar;file:///Users/Raghav/Desktop/DaftPunk/Resources/flink-connector-jdbc-3.1.0-1.17.jar")
    # t_env.get_config().set("pipeline.jars", "file:///Users/karanbawejapro/Desktop/jarfiles/flink-sql-connector-kafka-1.17.1.jar")
    t_env.get_config().set("table.exec.source.idle-timeout", "1000")

    
    # Mouse Clicks Source
    source_ddl_1 = """
        CREATE TABLE mouse_clicks(
            sessionId VARCHAR,
            event VARCHAR,
            timestamp_clicks BIGINT,
            timez_ltz AS TO_TIMESTAMP_LTZ(timestamp_clicks,3),
            WATERMARK FOR timez_ltz AS timez_ltz - INTERVAL '5' SECONDS
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'mouse_clicks',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'click_group',
            'scan.startup.mode' = 'specific-offsets',
            'scan.startup.specific-offsets' = 'partition:0,offset:0',
            'json.fail-on-missing-field' = 'false',
            'json.ignore-parse-errors' = 'true',
            'format' = 'json'
        )
        """    
    t_env.execute_sql(source_ddl_1)
    tbl_clicks = t_env.from_path('mouse_clicks')
    tbl_clicks.print_schema()
    # tbl_clicks.execute().print()

    
    # Building 3 tables for the 3 hopping windows of 5s, 10s and 30s
    window_clicks_5s_sql = """
        SELECT sessionId, window_start, window_end, CAST(COUNT(event) AS DECIMAL(10,2)) AS count_5s
        FROM TABLE(
        HOP(TABLE mouse_clicks, DESCRIPTOR(timez_ltz), INTERVAL '2.5' SECONDS, INTERVAL '5' SECONDS))
        GROUP BY sessionId, window_start, window_end;
    """
    table_5s = t_env.sql_query(window_clicks_5s_sql)

    window_clicks_10s_sql = """
        SELECT sessionId, window_start, window_end, CAST(COUNT(event) AS DECIMAL(10,2)) AS count_10s
        FROM TABLE(
        HOP(TABLE mouse_clicks, DESCRIPTOR(timez_ltz), INTERVAL '5' SECONDS, INTERVAL '10' SECONDS))
        GROUP BY sessionId, window_start, window_end;
    """
    table_10s = t_env.sql_query(window_clicks_10s_sql)

    window_clicks_30s_sql = """
        SELECT sessionId, window_start, window_end, CAST(COUNT(event) AS DECIMAL(10,2)) AS count_30s
        FROM TABLE(
        HOP(TABLE mouse_clicks, DESCRIPTOR(timez_ltz), INTERVAL '15' SECONDS, INTERVAL '30' SECONDS))
        GROUP BY sessionId, window_start, window_end;
    """
    table_30s = t_env.sql_query(window_clicks_30s_sql)
    
    
    # Registering the 3 Tables in the Flink SQL Catalog
    t_env.register_table("table_5s", table_5s)
    t_env.register_table("table_10s", table_10s)
    t_env.register_table("table_30s", table_30s)


    # Merging the processed clicks data and sending to Kafka in upsert fashion
    # First create sink then insert merged clicks data into the sink table    
    sink_kafka_clicks = """
            CREATE TABLE sink_kafka_clicks (
                sessionId VARCHAR,
                avg_count_5s DECIMAL(10,2),
                avg_count_10s DECIMAL(10,2),
                avg_count_30s DECIMAL(10,2),
                PRIMARY KEY (sessionId) NOT ENFORCED
            ) WITH (
                'connector' = 'upsert-kafka',
                'topic' = 'feature_clicks',
                'properties.bootstrap.servers' = 'localhost:9092',
                'key.format' = 'json',
                'value.format' = 'json'
            );
    """
    t_env.execute_sql(sink_kafka_clicks)

    merged_clicks = """
            INSERT INTO sink_kafka_clicks
            SELECT t1.sessionId AS sessionId,
                t1.a AS avg_count_5s,
                t2.b AS avg_count_10s,
                t3.c AS avg_count_30s
            FROM (SELECT sessionId, CAST(AVG(count_5s) AS DECIMAL(10, 2)) AS a FROM table_5s GROUP BY sessionId) t1
            LEFT JOIN (SELECT sessionId, CAST(AVG(count_10s) AS DECIMAL(10, 2)) as b FROM table_10s GROUP BY sessionId) t2
            ON t1.sessionId = t2.sessionId
            LEFT JOIN (SELECT sessionId, CAST(AVG(count_30s) AS DECIMAL(10, 2)) AS c FROM table_30s GROUP BY sessionId) t3
            ON t1.sessionId = t3.sessionId
    """
    t_env.execute_sql(merged_clicks).wait()


    # Cursor Source 
    # source_ddl_2 = """
    #     CREATE TABLE cursor_positions(
    #         sessionId VARCHAR,
    #         x INT,
    #         y INT,
    #         timestamp_cursor BIGINT
    #     ) WITH (
    #         'connector' = 'kafka',
    #         'topic' = 'cursor_positions',
    #         'properties.bootstrap.servers' = 'localhost:9092',
    #         'properties.group.id' = 'cursor_group',
    #         'scan.startup.mode' = 'specific-offsets',
    #         'scan.startup.specific-offsets' = 'partition:0,offset:0',
    #         'json.fail-on-missing-field' = 'false',
    #         'json.ignore-parse-errors' = 'true',
    #         'format' = 'json'
    #     )
    #     """  
    # t_env.execute_sql(source_ddl_2)
    # tbl_cursor = t_env.from_path('cursor_positions')
    # tbl_cursor.print_schema()
    # tbl_cursor.execute().print()


if __name__ == '__main__':
    log_processing()


# MySQL Sink Connector for Testing purposes
# sink_mysql = """
#     CREATE TABLE flink_final (
#     sessionId VARCHAR,
#     avg_count_5s DECIMAL(10,2),
#     avg_count_10s DECIMAL(10,2),
#     avg_count_30s DECIMAL(10,2),
#     PRIMARY KEY (sessionId) NOT ENFORCED
# ) WITH (
#     'connector' = 'jdbc',
#     'url' = 'jdbc:mysql://localhost:3306/flink',
#     'table-name' = 'flink_final',
#     'username' = 'root',
#     'password' = 'sw23'
# )
# """
# t_env.execute_sql(sink_mysql)
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import *
from pyflink.table.window import Tumble

def log_processing():

    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(env_settings)
    t_env.get_config().set("pipeline.jars", "file:///Users/Raghav/Desktop/DaftPunk/Resources/flink-sql-connector-kafka-1.17.1.jar")
    # t_env.get_config().set("pipeline.jars", "file:///Users/karanbawejapro/Desktop/jarfiles/flink-sql-connector-kafka-1.17.1.jar")
    t_env.get_config().set("table.exec.source.idle-timeout", "1000")

    # Mouse Clicks Source 
    source_ddl = """
        CREATE TABLE mouse_clicks(
            sessionId VARCHAR,
            event VARCHAR,
            timestamp_clicks BIGINT
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
    t_env.execute_sql(source_ddl)
    tbl = t_env.from_path('mouse_clicks')
    tbl.print_schema()
    tbl.execute().print()

    # windowed_clicks = (
    # tbl.window(Tumble.over(lit(5).seconds).on(col("timez_ltz")).alias("w"))
    # .group_by(col("sessionId"))
    # .select(
    #     col("sessionId").start.alias("window_start"),
    #     col("sessionId").end.alias("window_end"),
    #     col("event").count.alias("count")
    #     )
    # )

    # sink_ddl_print = """
    #     CREATE TABLE printx (
    #     `window_start` TIMESTAMP(3),
    #     `window_end` TIMESTAMP(3),
    #     `count` BIGINT
    # ) WITH (
    #     'connector' = 'print'
    # )
    # """
    # t_env.execute_sql(sink_ddl_print)
    # windowed_clicks.execute_insert('printx').wait()


if __name__ == '__main__':
    log_processing()
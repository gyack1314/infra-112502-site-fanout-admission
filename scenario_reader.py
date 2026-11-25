"""读取以输入时间排序的演练记录。"""

import argparse
import json
from pathlib import Path


def load_events(path, kinds):
    """逐行读取消息并保留原始业务数据。"""
    previous = -1
    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            try:
                event = json.loads(line)
                if not isinstance(event, dict) or set(event) != {"at", "kind", "record"}:
                    raise ValueError("每条记录需要 at、kind 和 record")
                timestamp = event["at"]
                if type(timestamp) is not int or timestamp < previous or timestamp < 0:
                    raise ValueError("消息秒点必须是非递减的非负整数")
                if event["kind"] not in kinds:
                    raise ValueError("未登记的消息名称")
                if not isinstance(event["record"], dict):
                    raise ValueError("record 必须为对象")
            except (TypeError, ValueError) as error:
                raise ValueError(f"{path.name} 第 {line_no} 行：{error}") from error
            previous = timestamp
            yield event


def show_samples(directory):
    """显示当前目录可读的演练文件。"""
    kinds = set(json.loads((directory / "message_types.json").read_text(encoding="utf-8")))
    examples = sorted(directory.glob("*.jsonl"))
    if not examples:
        raise ValueError("未找到演练文件")
    for path in examples:
        events = list(load_events(path, kinds))
        if not events:
            raise ValueError(f"{path.name} 没有消息")
        print(f"{path.name}　{len(events)} 条消息　{events[0]['at']} 至 {events[-1]['at']} 秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="浏览本地仿真消息")
    parser.add_argument("directory", type=Path)
    show_samples(parser.parse_args().directory)

# 工地服务网关的扇出预算与现场请求保供

诊断工作台向区域服务查询设备与维修资料。记录中的时间与供应能力均为合成数据，地区后端以仿真回执代替。

## 输入消息

每个 JSONL 文件是一段独立输入记录。每行包括整数秒点 at、消息名称 kind 与对象 record。at 代表中间件收到消息的时刻，同一秒内按行序提交。业务时间和对应回执引用写在 record 中。

- **capacity**　地区状态通知。pool 是总执行并发，per_service 是地区内各类服务自己允许的并发，floor 是仅急单可用的预留份额，初始 status 为 up。不是频率或每期可消费次数。 scope 为其可服务的矿区资料范围。
- **request**　客户以 id 提交请求，class 为 urgent 或 bulk，deadline 为最晚接收秒点。items 里的 service 为后端服务，required 标识是否必需。depends 是同一个请求中需要先得出结果的项，参数按 item 标识引用。 regions 按客户可用地区的偏好顺序列出，scope 为所需矿区资料范围。
- **reply**　后端回报指定 request、item、region 的一次实际派发结果。编号 attempt 从该请求同一项第一次到该地区的派发起计算。done 携带 value，stopped 说明工作最终停止，silent 仅代表当前无回执。
- **wake**　仿真钟推进。网关可根据当前时间和可用事项考虑新的派发。hedge_after 为请求允许考虑备选的最小等候，最短执行耗时由地区的 latency 提供。
- **cancel**　按 id 通知网关受理方已不需要该请求。
- **inspect**　按 request 或 region 读取值班视图。
- **restart**　模拟网关重启，后端仍保有此前接受的工作。

## 示例

- spare-capacity.jsonl
- ineligible-backups.jsonl

## 读取演练资料

运行环境为 Python 3.11，只使用标准库。在根目录运行以下命令可核对文件格式及读取接口。

    python3 scenario_reader.py examples
    python3 -m unittest discover -v

资料读取器会列出各文件包含的消息和时间范围。演练记录只描述各参与方交给系统的输入。

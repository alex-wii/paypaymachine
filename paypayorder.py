# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = paypay_order_from_dict(json.loads(json_string))
from dataclasses_json import dataclass_json
from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
import json


# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = pay_pay_order_from_dict(json.loads(json_string))



T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Content:
    cupnum: str
    stationa: str
    stationb: str
    stationc: str
    stationd: str
    statione: str
    stationf: str

    @staticmethod
    def from_dict(obj: Any) -> 'Content':
        assert isinstance(obj, dict)
        cupnum = from_str(obj.get("cupnum"))
        stationa = from_str(obj.get("stationa"))
        stationb = from_str(obj.get("stationb"))
        stationc = from_str(obj.get("stationc"))
        stationd = from_str(obj.get("stationd"))
        statione = from_str(obj.get("statione"))
        stationf = from_str(obj.get("stationf"))
        return Content(cupnum, stationa, stationb, stationc, stationd, statione, stationf)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cupnum"] = from_str(self.cupnum)
        result["stationa"] = from_str(self.stationa)
        result["stationb"] = from_str(self.stationb)
        result["stationc"] = from_str(self.stationc)
        result["stationd"] = from_str(self.stationd)
        result["statione"] = from_str(self.statione)
        result["stationf"] = from_str(self.stationf)
        return result

@dataclass_json
@dataclass
class PayPayOrder:
    ordernum: str
    cupcount: int
    content: List[Content]

    @staticmethod
    def from_dict(obj: Any) -> 'PayPayOrder':
        assert isinstance(obj, dict)
        ordernum = from_str(obj.get("ordernum"))
        cupcount = from_int(obj.get("cupcount"))
        content = from_list(Content.from_dict, obj.get("content"))
        return PayPayOrder(ordernum, cupcount, content)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ordernum"] = from_str(self.ordernum)
        result["cupcount"] = from_int(self.cupcount)
        result["content"] = from_list(lambda x: to_class(Content, x), self.content)
        return result


def pay_pay_order_from_dict(s: Any) -> PayPayOrder:
    return PayPayOrder.from_dict(s)


def pay_pay_order_to_dict(x: PayPayOrder) -> Any:
    return to_class(PayPayOrder, x)


def main():
    # order='{"ordernum":"RSAP21071400002","cupcount":1,"content":[{"cupnum":"A0001","stationa":"02","stationb":"01010200030004000500","stationc":"01010200030004000500","stationd":"01000200030004000503","statione":"01010200030004000500","stationf":"01010200030004000500"}]}'
    # orderjson = json.loads(order)
    # print(orderjson)
    # orderinfo=PayPayOrder.from_json(order)
    # # orderinfo=pay_pay_order_from_dict(order)
    # print(f'{orderinfo.content}')
    # print(f'{orderinfo.content[0].cupnum}')
    
    recp_dic = {"stationa":1,"stationb":2,"stationc":3,"stationd":4,"statione":5,"stationf":6,"s6":"endpoint"}
    station_dic = {"s0":"stationa","s1":"stationb","s2":"stationc","s3":"stationd","s4":"statione","s5":"stationf","s6":"endpoint"}
    station = ["s0","s1","s2","s3","s4","s5","s6"]
    print(station_dic['s0'])
    print(recp_dic['stationa'])
    print(recp_dic[station_dic['s0']])
    # for sta in station:
    #     print(recp_dic[station_dic[sta]])
if __name__ == '__main__':
    main()
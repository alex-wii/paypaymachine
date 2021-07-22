# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = pay_pay_cup_order_from_dict(json.loads(json_string))

from dataclasses_json import dataclass_json
from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

@dataclass_json
@dataclass
class PayPayCupOrder:
    cupnum: str
    stationa: str
    stationb: str
    stationc: str
    stationd: str
    statione: str
    stationf: str

    @staticmethod
    def from_dict(obj: Any) -> 'PayPayCupOrder':
        assert isinstance(obj, dict)
        cupnum = from_str(obj.get("cupnum"))
        stationa = from_str(obj.get("stationa"))
        stationb = from_str(obj.get("stationb"))
        stationc = from_str(obj.get("stationc"))
        stationd = from_str(obj.get("stationd"))
        statione = from_str(obj.get("statione"))
        stationf = from_str(obj.get("stationf"))
        return PayPayCupOrder(cupnum, stationa, stationb, stationc, stationd, statione, stationf)

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


def pay_pay_cup_order_from_dict(s: Any) -> PayPayCupOrder:
    return PayPayCupOrder.from_dict(s)


def pay_pay_cup_order_to_dict(x: PayPayCupOrder) -> Any:
    return to_class(PayPayCupOrder, x)

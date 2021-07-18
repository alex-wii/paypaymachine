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
    s0: str
    s1: str
    s2: str
    s3: str
    s4: str
    s5: str

    @staticmethod
    def from_dict(obj: Any) -> 'PayPayCupOrder':
        assert isinstance(obj, dict)
        cupnum = from_str(obj.get("cupnum"))
        s0 = from_str(obj.get("s0"))
        s1 = from_str(obj.get("s1"))
        s2 = from_str(obj.get("s2"))
        s3 = from_str(obj.get("s3"))
        s4 = from_str(obj.get("s4"))
        s5 = from_str(obj.get("s5"))
        return PayPayCupOrder(cupnum, s0, s1, s2, s3, s4, s5)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cupnum"] = from_str(self.cupnum)
        result["s0"] = from_str(self.s0)
        result["s1"] = from_str(self.s1)
        result["s2"] = from_str(self.s2)
        result["s3"] = from_str(self.s3)
        result["s4"] = from_str(self.s4)
        result["s5"] = from_str(self.s5)
        return result


def pay_pay_cup_order_from_dict(s: Any) -> PayPayCupOrder:
    return PayPayCupOrder.from_dict(s)


def pay_pay_cup_order_to_dict(x: PayPayCupOrder) -> Any:
    return to_class(PayPayCupOrder, x)

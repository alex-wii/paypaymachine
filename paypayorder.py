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
    s0: str
    s1: str
    s2: str
    s3: str
    s4: str
    s5: str

    @staticmethod
    def from_dict(obj: Any) -> 'Content':
        assert isinstance(obj, dict)
        cupnum = from_str(obj.get("cupnum"))
        s0 = from_str(obj.get("s0"))
        s1 = from_str(obj.get("s1"))
        s2 = from_str(obj.get("s2"))
        s3 = from_str(obj.get("s3"))
        s4 = from_str(obj.get("s4"))
        s5 = from_str(obj.get("s5"))
        return Content(cupnum, s0, s1, s2, s3, s4, s5)

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
    order='{"ordernum":"RSAP21071400002","cupcount":1,"content":[{"cupnum":"A0001","s0":"02","s1":"01010200030004000500","s2":"01010200030004000500","s3":"01000200030004000503","s4":"01010200030004000500","s5":"01010200030004000500"}]}'
    orderjson = json.loads(order)
    print(orderjson)
    orderinfo=PayPayOrder.from_json(order)
    # orderinfo=pay_pay_order_from_dict(order)
    print(f'{orderinfo.content=}')
    print(f'{orderinfo.content[0].cupnum=}')
if __name__ == '__main__':
    main()
from enum import Enum
from re import findall, fullmatch, match

class MDBlock(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE ="quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str):
    if match(r"^\#{1,6} ", block) is not None:
        return MDBlock.HEADING
    if match(r"(^```)(.|\n)*(```$)", block) is not None:
        return MDBlock.CODE
    if fullmatch(r"^>(.*\n>)*.*", block) is not None:
        return MDBlock.QUOTE
    if match(r"^- ", block) is not None:
        return MDBlock.UNORDERED_LIST
    if fullmatch(r"^1\. .*(\n\d+\. .*)*", block) is not None:
        nums = findall(r'(1\. |\n\d+\. )', block)
        for i in range(len(nums)):
            nums[i] = int(nums[i].strip("\n ."))
        if nums[0] == 1 and all(b == a + 1 for a, b in zip(nums, nums[1:])):
            return MDBlock.ORDERED_LIST
        raise Exception("Ordered list should start at 1 and then increase by one for each line")
    return MDBlock.PARAGRAPH
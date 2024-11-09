import time
from typing import List, Dict, Any

def is_valid_str(value:str) -> bool:
    '''check if given string is not None and length at least 1'''

    if isinstance(value, str):
        return value is not None and len(value) > 0
    return False

def timestamp() -> int:
    '''get current timestamp'''

    return int(time.time())

def date_yymmdd():
    '''get current date of yyyy-mm-dd'''

    return time.strftime('%Y-%m-%d')

def date_yymmdd_prettry():
    '''get current date of yyyy年mm月dd日'''

    return time.strftime('%Y - %m - %d')

def date_yesterday():
    '''get yesterday date'''

    return time.strftime('%Y-%m-%d', time.localtime(time.time() - 60 * 60 * 24))

def calc_page_count(total_count:int, page_count:int) -> int:
    '''计算总页数'''

    if total_count == 0:
        return 0
    if total_count % page_count == 0:
        return total_count // page_count
    return total_count // page_count + 1

def handle_pages(total_count:int, page_count:int, current_page:int, page_range=2) -> List[int]:
    '''获取分页列表，以当前页为中心，左右各取page_range页'''

    if total_count == 0:
        return []
    
    _page_count = calc_page_count(total_count, page_count)
    if _page_count <= 1:
        return [1]
    
    if current_page < 1:
        current_page = 1
    elif current_page > _page_count:
        current_page = _page_count
    
    _pages = [current_page]
    for i in range(1, page_range + 1):
        if current_page - i > 0:
            _pages.insert(0, current_page - i)
        if current_page + i <= _page_count:
            _pages.append(current_page + i)

    return _pages

def handle_pages_as_url(base:str, pages:List[int], current_page:int, postfix:str="") -> List[str]:

    _urls = []
    for page in pages:
        _urls.append(f"{base}/{page - 1}{postfix}" if page != current_page else "")
    return _urls


if __name__ == "__main__":
    print(timestamp())
from django.utils.safestring import mark_safe
import copy

"""
    <!-- 分頁 -->
    <ul class="pagination">
      
      {{page_string}}

   </ul>
    <!-- 分頁 -->
"""


class Pagenation(object):

    def __init__(self, request, queryset, page_size = 10, page_param="page", plus = 5):
        """
        :param request: 請求對象
        :param queryset: 符合條件數據
        :param page_size: 一頁面有多少分頁
        :param page_param: 在URL中獲取GET分頁的參數
        :param plus: 前後幾頁
        """
        #### 分頁與搜尋 使get獲得更多
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        #### 分頁與搜尋

        page = request.GET.get(page_param, "1")
        ## 確保輸入錯誤時拿到第一頁
        if page.isdecimal():
            self.page = int(page)
        else:
            self.page = 1

        
        # page parameters
        self.plus = plus
        self.page_size = page_size
        self.start = (self.page - 1) * self.page_size
        self.end = self.page * page_size

        self.page_queryset = queryset[self.start : self.end]

        # 總條數    
        total_count = queryset.count()
        total_pages_count, div = divmod(total_count, self.page_size)

        if div > 0:
            total_pages_count += 1

        self.total_pages_count = total_pages_count
        # 計算當前分業 自動5page first 5 page and last 5 page

    def html(self):
        
        if self.total_pages_count <= self.plus*2 + 1:
            start_page = 1
            end_page = self.total_pages_count
        else:
            # 判斷當前page是否超5page
            if self.page <= self.plus:
                start_page = 1
                end_page = self.plus * 2 + 1
            else:
                if self.page + self.plus > self.total_pages_count:
                    start_page = self.total_pages_count - self.plus * 2
                    end_page = self.total_pages_count

                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus + 1

        page_string =[]
        self.query_dict.setlist(self.page_param, [1])

        page_string.append(f'<li class=""><a href="?{self.query_dict.urlencode()}" aria-label="Previous"><span aria-hidden="true">首頁</span></a></li>')
        # previous page
        if self.page >1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            page_string.append(f'<li class=""><a href="?{self.query_dict.urlencode()}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>')
        else:
            self.query_dict.setlist(self.page_param, [1])
            page_string.append(f'<li class="disabled"><a href="?{self.query_dict.urlencode()}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>')
        


        # we can use mark safe to put the html code to front
        for i in range(start_page, end_page+1):
            query_dict_copy = copy.deepcopy(self.query_dict)
            query_dict_copy.setlist(self.page_param, [i])
            if i == self.page:
                
                page_string.append(f'<li class="active"><a href="?{query_dict_copy.urlencode()}">{i}</a></li>')
            else:
                page_string.append(f'<li><a href="?{query_dict_copy.urlencode()}">{i}</a></li>')

        # next page
        if self.page < self.total_pages_count:

            self.query_dict.setlist(self.page_param, [self.page + 1])

            page_string.append(f'<li class=""><a href="?{self.query_dict.urlencode()}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            
            self.query_dict.setlist(self.page_param, [self.total_pages_count])

            page_string.append(f'<li class=""><a href="?{self.query_dict.urlencode()}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
        
        # last page
        self.query_dict.setlist(self.page_param, [self.total_pages_count])
        page_string.append(f'<li class=""><a href="?{self.query_dict.urlencode()}" aria-label="Next"><span aria-hidden="true">Last Page</span></a></li>')
        page_string = mark_safe(''.join(page_string)) 
        return page_string

    
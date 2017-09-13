__author__ = 'Administrator'
from django.utils.safestring import mark_safe


class Page:
    #             当前所在页面   记录条数统计  页面显示记录数   显示的页面数量
    def __init__(self, current_page, data_count, per_page_count=10, pager_num=7):
        try:
            self.current_page = int(current_page)#当前当前所在页面
        except Exception as e:
            self.current_page = 1#如果为空就为1
        #self.current_page = current_page#当前当前所在页面
        self.data_count = data_count#记录条数统计
        self.per_page_count = per_page_count#页面显示记录数
        self.pager_num = pager_num#显示的页面数量

    #开始的记录数
    @property#装饰后 不用加()
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    #结束记录数
    @property
    def end(self):
        return self.current_page * self.per_page_count

    #计算当前所有数据 需要的总页面数
    @property
    def total_count(self):
      #商  余   商计算   记录条数统计  页面显示记录数
        v, y = divmod(self.data_count, self.per_page_count)
        if y:#如果有余数
            v += 1#页面数需加1
        return v

    #显示页面的方法函数 base_url为要跳转到的页面 ID
    def page_str(self, base_url):
        page_list = []#想要显示的页面列表
        #当 所有的页面数 小于  想要显示的页面数
        if self.total_count < self.pager_num:
            #从第一页开始
            start_index = 1
            #到最后一页
            end_index = self.total_count + 1

        else:
            ##当前所在页面数 小于等于  想要显示的页面数的 +1 的一半  ( 总页面数  大于 想要显示的页面数   应对最前面的页面显示)
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1#第一页面
                end_index = self.pager_num + 1#想要显示的页面
            else:
                #开始页面为选中页面的 前面几页(想要显示页面的+1的一半数, 选中页面保持中间位置 )
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
                #如果 当前所在页面数 + 显示页面的 - 1 的一半 大于总页面数,(应对最后面的显示)
                if (self.current_page + (self.pager_num - 1) / 2) > self.total_count:
                    start_index = self.total_count - self.pager_num + 1
                    end_index = self.total_count + 1

        #如果当前为1时
        if self.current_page == 1:
            #上一页不再跳转
            prev = '<li><a class="page" href="javascript:void(0);">上一页</a>'
        else:
            prev = '<li><a class="page" href="%s?p=%s">上一页</a>' % (base_url, self.current_page - 1,)
        page_list.append(prev)
        #循环  开始显示页面  结束显示页面
        for i in range(int(start_index), int(end_index)):
            #如果所选中的页面,加CSS样式
            if i == self.current_page:
                temp = '<li><a class="page active" href="%s?p=%s">%s</a>' % (base_url, i, i)
            else:
                temp = '<li><a class="page" href="%s?p=%s">%s</a>' % (base_url, i, i)
            page_list.append(temp)
        #如果当前所在页面 等于 最后的页面
        if self.current_page == self.total_count:
             #下一页不再跳转
            nex = '<li><a class="page" href="javascript:void(0);">下一页</a>'
        else:
            nex = '<li><a class="page" href="%s?p=%s">下一页</a>' % (base_url, self.current_page + 1,)
        page_list.append(nex)
        #跳转页面 input框
        # jump = """
        # <input type='text'  /><a onclick='jumpTo(this, "%s?p=");'>GO</a>
        # <script>
        #     function jumpTo(ths,base){
        #         var val = ths.previousSibling.value;
        #         location.href = base + val;
        #     }
        # </script>
        # """ % (base_url,)
        #
        # page_list.append(jump)#加入列表

        page_str = mark_safe("".join(page_list))#拼接列表为长字符串

        return page_str

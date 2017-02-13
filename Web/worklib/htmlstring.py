#这里文件定义了常用组合HTML代码的字符串

#排行榜HTML
STRING_HEAD_TITLE_RANKLIST = """<h2><strong>"""
STRING_MID_TITLE_RANKLIST = """</strong></h2>
                <table class="table table-striped table-hover ">
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>姓名</th>
                            <th>学院->教学科目</th>
                            <th>赞/不赞 -> 评分</th>
                        </tr>
                    </thead>
                    <tbody>"""
STRING_TAIL_RANKLIST = """</tbody>
                </table>
                """

WORDSTATUS_TABLE_BODY = """<tr><td>2</td><td>加载中...</td><td>加载中...</td><td>加载中...</td></tr><tr class="info"><td>3</td><td>加载中...</td><td>加载中...</td><td>加载中...</td></tr><tr class="success"><td>4</td><td>加载中...</td><td>加载中...</td><td>加载中...</td></tr>"""


#######下面的String是用于曝光台
BP_HEAD_INFO  = """<div class="panel panel-info">
  <div class="panel-heading">
    <h3 class="panel-title">"""

BP_HEAD_NORMAL  = """<div class="panel panel-success">
  <div class="panel-heading">
    <h3 class="panel-title">"""

BP_HEAD_HOT  = """<div class="panel panel-danger">
  <div class="panel-heading">
    <h3 class="panel-title">"""

BP_A_CONTENT  = """</h3>
  </div>
  <div class="panel-body">
      <div class="row" style="margin-left: 10px;margin-right: 10px;">"""


BP_B_DATE = """</div>
    <div class="row" style="text-align: right; margin-right: 12px;">
        <div class="col-md-8" style="text-align:left; margin-top: 15px;">
        <span class="label label-default">"""


BP_C_UPS = """</span>
        <span class="label label-default">"""

BP_D_LINK  = """ 人支持</span>
        <span class="label label-default">"""

BP_E_REPLYSUM = """条回复</span></div><div class="col-md-4">
        <a href="/badborad/"""

BP_TAIL  = """" class="btn btn-raised btn-primary" target="_blank">阅读更多</a>
    </div>
  </div>
</div></div>"""

#下面的代码用户曝光台的回复
RP_HEAD = """<div class="alert alert-dismissible alert-info">
                                        <div class="row">
                                            <span class="label label-primary" id="nickname_"""
RP_A_NICKNAME = """\">"""

RP_B_DATE = """</span>
                                            <span class="label label-default">"""

RP_C_REPLY = """</span>
                                            <span class="label label-success">
                                                <a href="#replydata" onclick="rpcontent('"""

RP_D_CONTENT_ID = """')">回复</a>
                                            </span>
                                        </div>
                                        <div id=\""""

RP_E_CONTENT = """\" class="row" style="margin-left: 5px;margin-right: 5px;margin-top: 2px;">"""

RP_TAIL = """</div>
                                    </div>"""


#下面的代码用于处理嵌套回复
IRP_SYM_HEAD = "@#9#6@"
IRP_SYM_TAIL = "@3#0#@"
IRP_HEAD = """<div class=\"panel-body innerreply\">"""
IRP_TAIL = """</div>"""
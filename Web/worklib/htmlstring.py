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
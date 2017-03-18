package com.kanchsproject.teacherrating;


import android.os.Looper;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import java.util.HashMap;
import java.util.Map;

public class WriteComment extends AppCompatActivity {

    private String URL_SUBMIT_COMMENTS = "http://115.159.197.66:5000/submitacomment";
    private String ID;
    private String NAME;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_write_comment);

        Button bts = (Button)findViewById(R.id.button_submit_comments);
        ID = getIntent().getStringExtra("ID");
        NAME  = getIntent().getStringExtra("NAME");
        bts.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                submitComments();
            }
        });
        setTitle("撰写评论->"+NAME);
    }


    private boolean submitComments(){
        //"http://115.159.197.66:5000/submitcomment/<int:id>/<comment>/";
        EditText etc = (EditText)findViewById(R.id.editText_comments);
        String comments = etc.getText().toString();
        if(comments.length() < 5)
        {
            Toast toast = Toast.makeText(this, getString(R.string.tips_comments_lessinfo), Toast.LENGTH_LONG);;toast.show();
            return false;
        }
        comments = comments.replace("\n","CSYZL");
        Button bts = (Button)findViewById(R.id.button_submit_comments);
        bts.setEnabled(false);
        //下面提交评论
        final String SUBMITURL = URL_SUBMIT_COMMENTS;
        final String COMMENT = comments;
        Thread td = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                try {
                    HttpUtils hu = new HttpUtils();
                    Map<String,String> data = new HashMap<String,String>();
                    data.put("id",ID);
                    data.put("comment",COMMENT);
                    String ddata = hu.submitPostData(SUBMITURL,data,"utf-8");
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        });
        td.start();
        while(td.getState() != Thread.State.TERMINATED)
        { ; }
        Log.v("submiturl=",SUBMITURL);
        Toast toast = Toast.makeText(this, getString(R.string.tips_update_ok), Toast.LENGTH_LONG);;toast.show();
        //提交完毕
        bts.setEnabled(true);
        return true;
    }
}

package com.kanchsproject.teacherrating;

import android.content.Context;
import android.os.Looper;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Arrays;

public class Comments extends AppCompatActivity {

    private Context context;
    private String URL_COMMENTS = "http://115.159.197.66:5000/getcomment/<int:id>/<int:linestart>/<int:lineend>/";
    private String UID = "";
    private String NAME = "";
    private Thread td = new Thread();

    private String Comments = new String();
    private String[] CommentsList;

    private ArrayAdapter<String> adapter;
    private ArrayList<String> commentslist  = new ArrayList<String>();

    private int StartPage = 0;
    private int Step = 10;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_comments);
        context = this;
        UID = getIntent().getStringExtra("TEACHERID");
        NAME = getIntent().getStringExtra("NAME");
        setTitle("其它学生对 "+NAME+" 的评论");
        //ListView lv = (ListView)findViewById(R.id.listView_data);
        getCommentsFromInternet(StartPage,StartPage+Step);
        getAsetCommentsLocal();
        getCommentsSum();

        Button btn = (Button)findViewById(R.id.button_next_page);
        Button btp = (Button)findViewById(R.id.button_last_page);
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onNextPage();
            }
        });
        btp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onPreviousPage();
            }
        });

    }

    private void onNextPage(){
        StartPage+=Step;
        try {
            getCommentsFromInternet(StartPage, StartPage + Step);
            getAsetCommentsLocal();
        }catch(Exception e){
            e.printStackTrace();
            Toast.makeText(context, getString(R.string.tips_retrive_no), Toast.LENGTH_LONG).show();
        }
    }

    private void onPreviousPage(){
        StartPage-=Step;
        try{
        getCommentsFromInternet(StartPage,StartPage+Step);
        getAsetCommentsLocal();
        }catch(Exception e){
            e.printStackTrace();
            Toast.makeText(context, getString(R.string.tips_retrive_no), Toast.LENGTH_LONG).show();
        }
    }

    private void getCommentsFromInternet(int pgstart,int pgend){
        String commentsURL = "http://115.159.197.66:5000/getcomment/";
        final String USER_RISGE_URL = commentsURL + UID + "/" + Integer.toString(pgstart) + "/" + Integer.toString(pgend) + "/";
        td = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                try {
                    WebClient wc = new WebClient();
                    String ddata = wc.getContent(USER_RISGE_URL,"utf-8",null);
                    Log.v("WRITE:", ddata);
                    writeToFile(context, ddata, "COMMENTS");
                }catch (Exception e){
                    e.printStackTrace();
                    Toast.makeText(context, getString(R.string.tips_retrive_no), Toast.LENGTH_LONG).show();
                }
            }
        });
        Toast.makeText(context, getString(R.string.tips_retriving_data), Toast.LENGTH_LONG).show();
        td.start();
    }

    private void getAsetCommentsLocal(){
        Thread ttd = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                while(td.getState() != Thread.State.TERMINATED)
                { ; }
                try {
                    Comments = readFromFile(context, "COMMENTS");
                    Log.v("orgComments", Comments);
                    CommentsList = Comments.split("<br/>");
                    int i = 0;
                    for (String x : CommentsList) {
                        CommentsList[i] = x.replace("CSYZL", "\r\n");
                    }
                }catch(Exception e){e.printStackTrace(); Toast.makeText(context, getString(R.string.tips_retrive_no), Toast.LENGTH_LONG).show();}
            }
        });
        ttd.start();
        while(td.getState() != Thread.State.TERMINATED){;}
        Toast.makeText(context, getString(R.string.tips_retrive_ok), Toast.LENGTH_LONG).show();
        ListView lv = (ListView)findViewById(R.id.listView_data);
        commentslist.clear();
        commentslist.addAll(Arrays.asList(CommentsList));
        adapter = new ArrayAdapter<String>(context, android.R.layout.simple_list_item_1,commentslist);
        lv.setAdapter(adapter);
        adapter.notifyDataSetChanged();
    }


    private void writeToFile(Context context, String data, String filename) {
        try {
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(context.openFileOutput(filename, Context.MODE_PRIVATE));
            outputStreamWriter.write(data);
            outputStreamWriter.close();
        }
        catch (IOException e) {
            e.getMessage();
        }
    }

    private String readFromFile(Context context,String filename) {

        String ret = "";

        try {
            InputStream inputStream = context.openFileInput(filename);

            if ( inputStream != null ) {
                InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
                String receiveString = "";
                StringBuilder stringBuilder = new StringBuilder();

                while ( (receiveString = bufferedReader.readLine()) != null ) {
                    stringBuilder.append(receiveString);
                }

                inputStream.close();
                ret = stringBuilder.toString();
            }
        }
        catch (FileNotFoundException e) {
            e.getMessage();
        } catch (IOException e) {
            e.getMessage();
        }
        return ret;
    }

    private void getCommentsSum(){
        Thread ttd = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                try{
                    WebClient wc = new WebClient();
                    String total = wc.getContent("http://115.159.197.66:5000/getcommentssum/"+ UID + "/","utf-8",null);
                    writeToFile(context,total,"CSUM");
                }catch (IOException e){
                    e.printStackTrace();
                }
            }
        });
        ttd.start();
        while(ttd.getState() != Thread.State.TERMINATED){;}
        String total = readFromFile(context,"CSUM");
        total = total.replace("(","");
        total = total.replace(")","");
        total = total.replace(",","");
        TextView tv = (TextView)findViewById(R.id.textView_comments_sum);
        tv.setText("评论总数："+ total);
    }

}

package com.kanchsproject.teacherrating;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Looper;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class TeacherInfo extends AppCompatActivity {

    private  String CACHE_FILE_NAME = "TD";
    private String TEACHER_ID;
    private String[] TD;
    private String RATINGLIST;
    private String COMMENTEDLIST;
    private String UID;
    private  String INFO_URL = "http://115.159.197.66:5000/getinfo/";
    private String URL_LIKE = "http://115.159.197.66:5000/addlike/";
    private String URL_DISLIKE = "http://115.159.197.66:5000/adddislike/";

    private Context context;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.teacher);
        context = this;
        UID = getIntent().getStringExtra("UID");

        Button bls = (Button)findViewById(R.id.button_likes);
        Button bds = (Button)findViewById(R.id.button_dislikes);
        Button baddcmt = (Button)findViewById(R.id.button_write_a_comment);
        Button bgetcmt = (Button)findViewById(R.id.button_showcomments);
        Button bfli = (Button)findViewById(R.id.button_fill_lost_info);

        bls.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onLike();
            }
        });
        bds.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onDislike();
            }
        });
        baddcmt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showWriteCommentsActivity();
            }
        });
        bgetcmt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showCommentsActivity();
            }
        });
        bfli.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showFillLostInfoActivity();
            }
        });

        getRatingList(UID);
        setInfo(CACHE_FILE_NAME);
       // /*/
        RATINGLIST = readFromFile(context, "RATINGLIST");
        Log.v("RATINGLIST=", RATINGLIST);
        if(RATINGLIST.indexOf(":") >=0) {
            int SET = 0;
            int XSTART = RATINGLIST.indexOf(TEACHER_ID);
            String SUFX = RATINGLIST.substring(XSTART + TEACHER_ID.length(), XSTART + TEACHER_ID.length()+1);
            String PREX = new String();
            if (XSTART > 0) {
                PREX = RATINGLIST.substring(XSTART - 1, XSTART);
            }
            if (XSTART != -1 && SUFX.equals(":") && (PREX.length() == 0 || PREX.equals(",")))   //ID:VAL,ID:VAL,ID:VAL
            {
                String[] rls = RATINGLIST.split(",");
                for (String X : rls) {
                    String[] el = X.split(":");
                    Log.v("str(el[])=(teacherID)", X + "," + TEACHER_ID);
                    Log.v("el[]data,el[0],el[1]=", el[0] + "," + el[1]);
                    if (el[0].equals(TEACHER_ID)) {
                        if (el[1].equals("L")) {
                            SET = 10;
                        } else if (el[1].equals("D")) {
                            SET = 100;
                        }
                    }
                }
                if (SET == 10) {
                    Log.v("SET?-----", "SET=10");
                    ((TextView) findViewById(R.id.button_likes)).setBackgroundColor(Color.YELLOW);
                    ((TextView) findViewById(R.id.button_dislikes)).setBackgroundColor(Color.TRANSPARENT);
                    ((TextView) findViewById(R.id.button_likes)).setEnabled(false);
                } else if (SET == 100) {
                    Log.v("SET?-----", "SET=100");
                    ((TextView) findViewById(R.id.button_dislikes)).setBackgroundColor(Color.YELLOW);
                    ((TextView) findViewById(R.id.button_likes)).setBackgroundColor(Color.TRANSPARENT);
                    ((TextView) findViewById(R.id.button_dislikes)).setEnabled(false);
                }
            }///*/
        }

    }

    private void showCommentsActivity(){
        Intent intent = new Intent(context, Comments.class);
        intent.putExtra("TEACHERID", TEACHER_ID);
        intent.putExtra("NAME",TD[1]);
        startActivity(intent);
    }

    private void showWriteCommentsActivity(){
        Intent intent = new Intent(context, WriteComment.class);
        intent.putExtra("ID", TEACHER_ID);
        intent.putExtra("NAME",TD[1]);
        startActivity(intent);
    }

    private void showFillLostInfoActivity(){
        Intent intent = new Intent(context, FillLostInfo.class);
        intent.putExtra("ID", TEACHER_ID);
        intent.putExtra("NAME",TD[1]);
        intent.putExtra("SUBJECT", TD[5]);
        intent.putExtra("SCHOOL", TD[6]);
        intent.putExtra("GENDER", TD[7]);
        startActivity(intent);
    }

    private void setInfo(String filename) {
        String data = readFromFile(context,filename);
        Log.v("setInfo=",data);
        data = data.replace("(","");
        data = data.replace(")","");
        data = data.replace("'","");
        TD = data.split(",");
        //(1,   'Dan', 0.0,     0,      0,   '未知', '未知', 0)
        // ID   NAME  SCORE  LIEKS DISLIKES SUBJECT SCHOOL GENDER
        // 0     1      2       3       4       5       6   7
        Log.v("data",data);
        TEACHER_ID = TD[0];
        ((TextView)findViewById(R.id.textView_name)).setText(getString(R.string.layout_info_name)+ ":" + TD[1]);
        ((TextView)findViewById(R.id.textView_subject)).setText(getString(R.string.layout_info_subject)+ ":" + TD[5]);
        ((TextView)findViewById(R.id.textView_school)).setText(getString(R.string.layout_info_school)+ ":" + TD[6]);
        ((TextView)findViewById(R.id.button_likes)).setText(getString(R.string.layout_info_like)+ "(" + TD[3] + ")");
        ((TextView)findViewById(R.id.button_dislikes)).setText(getString(R.string.layout_info_dislike)+ "(" + TD[4] + ")");
        if(TD[7] == "0")
        {
            ((TextView)findViewById(R.id.textView_gender)).setText("女");
        }else{
            ((TextView)findViewById(R.id.textView_gender)).setText("男");
        }
    }
    private void updateInfo(){
        final String np = INFO_URL + TEACHER_ID + "/";
        Thread td = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                try {
                    WebClient wc = new WebClient();
                    String ddata = wc.getContent(np,"utf-8",null);
                    ddata = ddata.replace("<br/>","");
                    Log.v("updateInfo:", ddata);
                    writeToFile(context, ddata, CACHE_FILE_NAME);
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        });
        td.start();
        while(td.getState() != Thread.State.TERMINATED)
        {  ;  }
        setInfo(CACHE_FILE_NAME);
    }

    private boolean onLike(){

        Thread td = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                try {
                    WebClient wc = new WebClient();
                    String ddata = wc.getContent(URL_LIKE +  UID + "/" + TEACHER_ID + "/", "utf-8", null);
                }catch(IOException e){ e.printStackTrace();}
            }
        });
        td.start();
        ((TextView)findViewById(R.id.button_likes)).setEnabled(false);
        ((TextView)findViewById(R.id.button_dislikes)).setEnabled(false);
        while(td.getState() != Thread.State.TERMINATED)
        { ; }
        updateInfo();
        ((TextView)findViewById(R.id.button_likes)).setEnabled(false);
        ((TextView)findViewById(R.id.button_dislikes)).setEnabled(true);
        ((TextView)findViewById(R.id.button_likes)).setBackgroundColor(Color.YELLOW);
        ((TextView)findViewById(R.id.button_dislikes)).setBackgroundColor(Color.TRANSPARENT);
        return true;
    }

    private boolean onDislike(){
        final Context context = this;
        Thread td = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                String ddata = new String();
                try {
                    WebClient wc = new WebClient();
                    ddata = wc.getContent(URL_DISLIKE +  UID + "/" + TEACHER_ID + "/", "utf-8", null);
                    writeToFile(context,ddata,"STATUS_DISLIKE");
                }catch(IOException e){ e.printStackTrace();}
            }
        });
        td.start();
        ((TextView)findViewById(R.id.button_dislikes)).setEnabled(false);
        ((TextView)findViewById(R.id.button_likes)).setEnabled(false);
        while(td.getState() != Thread.State.TERMINATED)
        { ; }
        updateInfo();
        ((TextView)findViewById(R.id.button_dislikes)).setEnabled(false);
        ((TextView)findViewById(R.id.button_likes)).setEnabled(true);
        ((TextView)findViewById(R.id.button_dislikes)).setBackgroundColor(Color.YELLOW);
        ((TextView)findViewById(R.id.button_likes)).setBackgroundColor(Color.TRANSPARENT);
        return true;
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

    private void getRatingList(String UID){
        String RatingListBaseURL = "http://115.159.197.66:5000/getratinglist/";
        final String REQUEST_URL = RatingListBaseURL + UID + "/";
        Thread td = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                try {
                    WebClient wc = new WebClient();
                    String ddata = wc.getContent(REQUEST_URL,"utf-8",null);
                    Log.v("WRITE:", ddata);
                    writeToFile(context, ddata, "RATINGLIST");
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        });
        td.start();
        while(td.getState() != Thread.State.TERMINATED){;}
    }
}

package com.kanchsproject.teacherrating;

import android.Manifest;
import android.app.Activity;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Looper;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.security.Permission;

public class MainActivity extends AppCompatActivity {

    private  Context context;
    private Thread td = new Thread();
    private boolean REFRESH_STATUS = true;
    final private int REQUEST_READ_PHONE_STATE = 0;
    private  String CACHE_FILE_NAME = "TD";
    private String UID = "";
    private  String INFO_URL = "http://115.159.197.66:5000/getinfo/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        context = this;
        if( !fileExists(this,"UID") )
        {
            if(android.os.Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                requestPermission();
            }else {
                UID = getIMEI();
                Log.v("UID=", UID);
                writeToFile(this, UID, "UID");
            }
        }else{ UID = readFromFile(this,"UID"); Log.v("UID=",UID);}
        Button bse = (Button)findViewById(R.id.button_search);
        bse.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                OnSearch();
            }
        });
    }


    public void OnSearch(){
        EditText etn = (EditText)findViewById(R.id.editText_teacher_name);
        String name = etn.getText().toString();
        String xname = name.replace(" ","");
        if(name.length() == 0 || xname.length()==0)
        {
            Toast toast = Toast.makeText(this, getString(R.string.tips_enter_name), Toast.LENGTH_LONG);;toast.show();
            return ;
        }
        getResult(name);
        Thread tt = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                while (td.getState() != Thread.State.TERMINATED)
                {     }
                if(REFRESH_STATUS != true) {
                    Toast toast = Toast.makeText(context, getString(R.string.tips_no_internet), Toast.LENGTH_LONG);;toast.show();
                }else{
                    Intent intent = new Intent(context, TeacherInfo.class);
                    intent.putExtra("UID", UID);
                    //intent.putExtra("CONTEXT",newslist.get(position));
                    startActivity(intent);
                }
            }
        });
        tt.start();
    }


    private void  getResult(String name){
        final String np = INFO_URL + name;
        td = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                try {
                    WebClient wc = new WebClient();
                    String ddata = wc.getContent(np,"utf-8",null);
                    ddata = ddata.replace("<br/>","");
                    Log.v("WRITE:", ddata);
                    writeToFile(context, ddata, CACHE_FILE_NAME);
                    REFRESH_STATUS = true;
                }catch (Exception e){
                    e.printStackTrace();
                    REFRESH_STATUS = false;
                }
            }
        });
        td.start();
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

    public boolean fileExists(Context context, String filename) {
        File file = context.getFileStreamPath(filename);
        if(file == null || !file.exists()) {
            return false;
        }
        return true;
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

    private void getCommentedList(String UID){
         String CommentedListBaseURL = "http://115.159.197.66:5000/getcommentedlist/";
        final String REQUEST_URL = CommentedListBaseURL + UID;
                Thread td = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                try {
                    WebClient wc = new WebClient();
                    String ddata = wc.getContent(REQUEST_URL,"utf-8",null);
                    Log.v("WRITE:", ddata);
                    writeToFile(context, ddata, "COMMENTEDLIST");
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        });
        td.start();
    }

    private void requestPermission(){
        int permissionCheck = ContextCompat.checkSelfPermission(this, Manifest.permission.READ_PHONE_STATE);

        if (permissionCheck != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.READ_PHONE_STATE}, REQUEST_READ_PHONE_STATE);
        } else {
            //TODO
        }
    }

    private  String getIMEI(){
        TelephonyManager mTelephonyMgr = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
        String imei = mTelephonyMgr.getDeviceId();
        return imei;
    }

    private void registeUser(String UID){
        String RegisteURL = "http://115.159.197.66:5000/registeuser/";
        final String USER_RISGE_URL = RegisteURL + UID + "/";
        Thread td = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                try {
                    WebClient wc = new WebClient();
                    String ddata = wc.getContent(USER_RISGE_URL,"utf-8",null);
                    Log.v("WRITE:", ddata);
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        });
        td.start();
        while(td.getState() != Thread.State.TERMINATED){;}
        getRatingList(UID);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch (requestCode) {
            case REQUEST_READ_PHONE_STATE:
                if ((grantResults.length > 0) && (grantResults[0] == PackageManager.PERMISSION_GRANTED)) {
                    //TODO
                    UID = getIMEI();
                    writeToFile(this,UID,"UID");
                    registeUser(UID);
                    Log.v("UID=", UID);
                }
                break;
            default:
                break;
        }
    }
}

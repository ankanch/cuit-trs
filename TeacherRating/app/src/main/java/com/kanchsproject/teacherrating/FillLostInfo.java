package com.kanchsproject.teacherrating;

import android.content.Context;
import android.os.Looper;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.view.menu.SubMenuBuilder;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

import java.util.HashMap;
import java.util.Map;

public class FillLostInfo extends AppCompatActivity {

    private String ID;
    private String NAME;
    private String SUBJECT;
    private String SCHOOL;
    private String GENDER;
    private Context contenxt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fill_lost_info);
        contenxt = this;

        ID = getIntent().getStringExtra("ID");
        NAME = getIntent().getStringExtra("NAME");
        SUBJECT = getIntent().getStringExtra("SUBJECT");
        SCHOOL = getIntent().getStringExtra("SCHOOL");
        GENDER = getIntent().getStringExtra("GENDER");

        setTitle("补全/修改信息:" + NAME);

        setInfo();
        Button btsubmit = (Button) findViewById(R.id.button_submit_fill);
        btsubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                CheckBox cb = (CheckBox)findViewById(R.id.checkBox_promise);
                if(!cb.isChecked()){
                    Toast toast = Toast.makeText(contenxt, "提交失败！请保证信息真实可靠！", Toast.LENGTH_LONG);
                    toast.show();
                }else {
                    submitInfo();
                }
            }
        });
    }

    private void setInfo() {
        EditText edsubject = (EditText) findViewById(R.id.editText_subjects);
        EditText edschool = (EditText) findViewById(R.id.editText_school);
        RadioButton rbfemale = (RadioButton) findViewById(R.id.radioButton_female);
        RadioButton rbmale = (RadioButton) findViewById(R.id.radioButton_male);

        edsubject.setText(SUBJECT);
        edschool.setText(SCHOOL);
        if (GENDER == "0") {
            rbmale.setChecked(true);
            rbfemale.setChecked(false);
        } else {
            rbfemale.setChecked(true);
            rbmale.setChecked(false);
        }
    }

    private void submitInfo() {
        Button btsubmit = (Button) findViewById(R.id.button_submit_fill);
        EditText edsubject = (EditText) findViewById(R.id.editText_subjects);
        EditText edschool = (EditText) findViewById(R.id.editText_school);
        RadioButton rbfemale = (RadioButton) findViewById(R.id.radioButton_female);
        RadioButton rbmale = (RadioButton) findViewById(R.id.radioButton_male);
        SUBJECT = edsubject.getText().toString();
        SCHOOL = edschool.getText().toString();
        if (rbfemale.isChecked()) {
            GENDER = "0";
        } else {
            GENDER = "1";
        }
        btsubmit.setEnabled(false);
        //下面提交
        final String SUBMIT_URL = "http://115.159.197.66:5000/filllostinfo";
        Thread td = new Thread(new Runnable() {
            @Override
            public void run() {
                Looper.prepare();
                try {
                    HttpUtils hu = new HttpUtils();
                    Map<String, String> data = new HashMap<String, String>();
                    data.put("id", ID);
                    data.put("subject", SUBJECT);
                    data.put("school", SCHOOL);
                    data.put("gender", GENDER);
                    String ddata = hu.submitPostData(SUBMIT_URL, data, "utf-8");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
        td.start();
        while (td.getState() != Thread.State.TERMINATED) {;}
        Log.v("submiturl=",SUBMIT_URL);
        Toast toast = Toast.makeText(this, getString(R.string.tips_update_ok), Toast.LENGTH_LONG);
        toast.show();
        //提交完毕
        btsubmit.setEnabled(true);
    }
}

package com.example.demoapp;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void login(View view) {
        EditText usernameV = (EditText)findViewById(R.id.username);
        EditText passwordV = (EditText)findViewById(R.id.password);
        String username = usernameV.getText().toString();
        String password = passwordV.getText().toString();

        boolean flag = false;
        if(!username.isEmpty() && !password.isEmpty()) {
            if(username.equals("madhuri") && password.equals("1234"))
                flag = true;
        }
        if(flag) {
            Intent navigate= new Intent(MainActivity.this, ViewActivity.class);
            startActivity(navigate);
        } else {
            new AlertDialog.Builder(MainActivity.this)
                    .setMessage("Incorrect credentials")
                    .setCancelable(true)
                    .setPositiveButton(
                            "OK", (dialog, id) -> dialog.cancel())
                    .show();
        }

    }
}
package com.example.client;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Html;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private Button btnSend;
    private EditText messageEditText;
    private TextView messageTextView;

    private static final String HOST = "192.168.137.1";
    private static final int PORT = 6547;

    PrintWriter output;
    Socket socket;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btnSend = findViewById(R.id.btnSend);
        messageEditText = findViewById(R.id.messageEditText);
        messageTextView = findViewById(R.id.messageTextView);
        messageTextView.setMovementMethod(new ScrollingMovementMethod());

        btnSend.setOnClickListener(this);

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    socket = new Socket(HOST, PORT);
                } catch (Exception e) {

                }
            }
        }).start();


        new Thread(new Runnable() {

            @Override
            public void run() {
                int indexOfMessage = 0;
                messageTextView.setText("");
                while (true) {
                    try {
                        Socket socket = new Socket(HOST, PORT);
                        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                        StringBuilder response = new StringBuilder();
                        String line;
                        indexOfMessage += 1;
                        while ((line = in.readLine()) != null) {
                            response.append("  " + line);
                        }
                        line = messageTextView.getText().toString() + "Message: " + String.valueOf(indexOfMessage) + response + "\n";
                        messageTextView.setText(line);
                        socket.close();
                        in.close();
                    } catch (Exception e) {}
                }
            }
        }).start();

    }

    public void onClick(View v) {

        Toast toast;
        if (v.getId() == R.id.btnSend) {
            try {
                toast = Toast.makeText(getApplicationContext(), "Sending Data to PC...", Toast.LENGTH_SHORT);
                toast.show();

                output = new PrintWriter(socket.getOutputStream());
                output.print(messageEditText.getText().toString().trim());
                output.flush();

                toast = Toast.makeText(getApplicationContext(), "Data sent to PC...", Toast.LENGTH_SHORT);
                toast.show();

            } catch (Exception e) {
                toast = Toast.makeText(getApplicationContext(), "Error happened:\nMake sure you are connected to hotspot\nServer is open", Toast.LENGTH_SHORT);
                toast.show();
            }
        }
    }
}

package luke.com.fiirapp;

import android.Manifest;
import android.app.Activity;
import android.app.ActivityOptions;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v4.content.FileProvider;
import android.support.v4.view.GestureDetectorCompat;
import android.util.Log;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import static android.Manifest.*;
import static android.Manifest.permission.*;

public class MainActivity extends Activity {

    Button tab1;
    Button tab2;
    Button tab3;
    RelativeLayout cameraButton;
    ArrayList<Button> tabs;
    TextView infoText;
    TextView buttonText;
    ScrollView scrollView;

    private GestureDetectorCompat detector;
    private ApiRequest apiRequest;
    private static final int ACTION_TAKE_PHOTO_B = 1;
    private static final int ACTION_TAKE_PHOTO_S = 2;
    private static final int ACTION_TAKE_VIDEO = 3;

    final String DEBUG = "MainActivity";
    final int PERMISSION_GRANTED = PackageManager.PERMISSION_GRANTED;
    final int REQUEST_CAMERA_PERMISSION = 1;
    final int REQUEST_WRITE_PERMISSION = 2;
    final int REQUEST_INTERNET_PERMISSION = 3;
    int[] permissionResults;    // results from permission requests
    int state;
    int FIIR_Red;
    String photoPath;

    public MainActivity() {
        state = 0;
        FIIR_Red = Color.parseColor("#820000");
        tabs = new ArrayList<>();
        photoPath = "";
        permissionResults = new int[]{0, 0, 0};
        apiRequest = new ApiRequest("http://fiirapp.ddns.net:9096");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tab1 = (Button) findViewById(R.id.tab1);
        tab2 = (Button) findViewById(R.id.tab2);
        tab3 = (Button) findViewById(R.id.tab3);
        cameraButton = (RelativeLayout) findViewById(R.id.button);

        tabs.add(tab1);
        tabs.add(tab2);
        tabs.add(tab3);

        scrollView = (ScrollView) findViewById(R.id.scrollView);
        buttonText = (TextView) findViewById(R.id.button_text);
        infoText = (TextView) findViewById(R.id.textView);
        infoText.setTypeface(Typeface.createFromAsset(getAssets(), "hnt.ttf"));
        buttonText.setTypeface(Typeface.createFromAsset(getAssets(), "hn.ttf"));

        tab1.setOnClickListener(this::tabOne);
        tab2.setOnClickListener(this::tabTwo);
        tab3.setOnClickListener(this::tabThree);
        cameraButton.setOnClickListener(this::onCameraButtonPress);

        for (Button b : tabs) {
            b.setTypeface(Typeface.createFromAsset(getAssets(), "hn.ttf"));
        }

        detector = new GestureDetectorCompat(this, new gestureListener());
    }


    // TODO request camera and storage permissions
    private void onCameraButtonPress(View view) {
        if(ContextCompat.checkSelfPermission(this,CAMERA) == PERMISSION_GRANTED
            && ContextCompat.checkSelfPermission(this, WRITE_EXTERNAL_STORAGE) == PERMISSION_GRANTED
            && ContextCompat.checkSelfPermission(this, INTERNET) == PERMISSION_GRANTED){
            openCamera(view);
        } else {
            if(ContextCompat.checkSelfPermission(this,CAMERA)!=PERMISSION_GRANTED){
                Log.i(DEBUG, "requesting camera permission");
                ActivityCompat.requestPermissions(this,
                        new String[]{permission.CAMERA},
                        REQUEST_CAMERA_PERMISSION);
            }

            if(ContextCompat.checkSelfPermission(this,WRITE_EXTERNAL_STORAGE)!=PERMISSION_GRANTED){
                Log.i(DEBUG, "requesting write permission");
                ActivityCompat.requestPermissions(this,
                        new String[]{permission.WRITE_EXTERNAL_STORAGE},
                        REQUEST_WRITE_PERMISSION);
            }

            if(ContextCompat.checkSelfPermission(this,INTERNET) != PERMISSION_GRANTED){
                Log.i(DEBUG, "requesting internet permission");
                ActivityCompat.requestPermissions(this,
                        new String[]{permission.INTERNET},
                        REQUEST_INTERNET_PERMISSION);
            }
        }
    }

    //
    private void openCamera(View view) {
        Log.i(DEBUG, "opening camera");
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        // Ensure that there's a camera activity to handle the intent
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            // Create the File where the photo should go
            File photoFile = null;
            try {
                Log.i(DEBUG, "creating image file");
                photoFile = createImageFile();
            } catch (IOException e) {
                Log.e(DEBUG, "IOException thrown");
                e.printStackTrace();
            }
            // Continue only if the File was successfully created
            if (photoFile != null) {
                Log.i(DEBUG, "file path: " + photoFile.getAbsolutePath());
                Log.i("external storage dir", Environment.getExternalStorageDirectory().toString());
                Uri photoURI = FileProvider.getUriForFile(this,
                        "luke.com.fiirapp.fileprovider",
                        photoFile);
                Log.i("tag", "got photo uri");
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                Log.e(DEBUG, "starting camera for pic result");

                if(ContextCompat.checkSelfPermission(this,Manifest.permission.INTERNET) ==
                        PackageManager.PERMISSION_GRANTED){
                    Log.i("INTERNET", "has internet permission");
                } else {
                    Log.i("INTERNET", "does not have internet permission");
                }


                startActivityForResult(takePictureIntent, 1);
            }
        } else {
            Log.wtf(DEBUG, "camera activity not found!");
        }
    }

    // creates unique temporary file path for later use
    private File createImageFile() throws IOException {
        // Create an image file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = timeStamp + "_" + PhotoFileHelper.getRandomString(10);
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        photoPath = image.getAbsolutePath();
        return image;
    }

    @Override
    // TODO send intent to ApproveActivity
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // save file to dcim
        if (photoPath != null) {
            //setPic();
            galleryAddPic();

            File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
            try {
                File tempFile = File.createTempFile(
                        "temp",  /* prefix */
                        ".jpg",         /* suffix */
                        storageDir      /* directory */
                );

                // try to publish to server
                PhotoFileHelper.publishPhoto(photoPath, tempFile.getAbsolutePath());
            } catch(IOException e){
                e.printStackTrace();
            }

            photoPath = null;
        }

        /*
        Intent intent = new Intent(getApplicationContext(), ApproveActivity.class);
        intent.putExtra("data", (Bitmap)data.getExtras().get("data"));
        scrollView.getContext().startActivity(intent);
        */
    }

    private void galleryAddPic() {
        Intent mediaScanIntent = new Intent("android.intent.action.MEDIA_SCANNER_SCAN_FILE");
        Uri contentUri = Uri.fromFile(new File(photoPath));
        mediaScanIntent.setData(contentUri);
        this.sendBroadcast(mediaScanIntent);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event){
        detector.onTouchEvent(event);
        return super.onTouchEvent(event);
    }

    @Override
    public void onRequestPermissionsResult(
            int requestCode, String permissions[], int[] results) {
        switch (requestCode){
            case REQUEST_CAMERA_PERMISSION:
                if(results.length > 0 && results[0] == PERMISSION_GRANTED){
                    // permission granted
                    permissionResults[0] = 1;
                } else {
                    // permission denied
                    permissionResults[0] = -1;
                }
                break;
            case REQUEST_WRITE_PERMISSION:
                if(results.length > 0 && results[0] == PERMISSION_GRANTED){
                    // permission granted
                    permissionResults[1] = 1;
                } else {
                    // permission denied
                    permissionResults[1] = -1;
                }
                break;
            case REQUEST_INTERNET_PERMISSION:
                if(results.length > 0 && results[0] == PERMISSION_GRANTED){
                    // permission granted
                    permissionResults[2] = 1;

                    // we have all permissions
                    if(permissionResults[0] == 1 && permissionResults[1] == 1){
                        openCamera(scrollView);
                    }
                } else {
                    // permission denied
                    permissionResults[0] = -1;
                }
                break;
        }
    }

    void tabOne(View view){
        tabs.get(state).setTextColor(Color.WHITE);
        tabs.get(state).setBackgroundColor(0);
        state = 0;
        tabs.get(state).setBackgroundColor(Color.WHITE);
        tabs.get(state).setTextColor(FIIR_Red);

        infoText.setText("$1 stream");
    }
    void tabTwo(View view){
        tabs.get(state).setTextColor(Color.WHITE);
        tabs.get(state).setBackgroundColor(0);
        state = 1;
        tabs.get(state).setBackgroundColor(Color.WHITE);
        tabs.get(state).setTextColor(FIIR_Red);

        infoText.setText("$100 stream");
    }
    void tabThree(View view){
        tabs.get(state).setTextColor(Color.WHITE);
        tabs.get(state).setBackgroundColor(0);
        state = 2;
        tabs.get(state).setBackgroundColor(Color.WHITE);
        tabs.get(state).setTextColor(FIIR_Red);

        infoText.setText("$1k stream");
    }
    void openSettings(){
        Intent intent = new Intent(getApplicationContext(), SettingsActivity.class);
        scrollView.getContext().startActivity(intent);

        if(android.os.Build.VERSION.SDK_INT >= 21) {
            overridePendingTransition(R.anim.slide_in_right, android.R.anim.fade_out);
        }
    }
    class gestureListener extends GestureDetector.SimpleOnGestureListener {
        private static final String DEBUG_TAG = "Gestures";

        @Override
        public boolean onDown(MotionEvent event) {
            return true;
        }

        @Override
        public boolean onFling(MotionEvent event1, MotionEvent event2,
                               float velocityX, float velocityY) {
            String DEBUG_TAG = "onFling";
            if(Math.abs(velocityX) > Math.abs(velocityY)){
                if(velocityX > 0){
                    Log.d(DEBUG_TAG, "Fling right");
                    switch (state){
                        case 0:
                            openSettings();
                            break;
                        case 1:
                            tabOne(null);
                            break;
                        case 2:
                            tabTwo(null);
                            break;
                    }
                }else{
                    Log.d(DEBUG_TAG, "Fling left");
                    switch (state){
                        case 0:
                            tabTwo(null);
                            break;
                        case 1:
                            tabThree(null);
                            break;
                        case 2:
                            break;
                    }
                }
            }

            return true;
        }// end onFling method
    }// end of gestureListener subclass
}

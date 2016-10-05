package luke.com.fiirapp;

import android.app.Activity;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;

/**
 * Created by luke on 10/4/16.
 */

public class ApproveActivity extends Activity {

    Bundle extras;
    ImageView preview;
    ApiRequest request;

    public ApproveActivity(){
        this.request = new ApiRequest("fiirapp.ddns.net");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_approve);

        preview = (ImageView) findViewById(R.id.preview_thumb);

        extras = getIntent().getExtras();
        if(extras != null){
            Bitmap thumb = (Bitmap)extras.get("data");
            preview.setImageBitmap(thumb);
        } else {
            // uh oh, no image received!
        }
    }

    void cancel(View view){

    }

    // for now, just post image and return
    // TODO add business logic for EditActivity
    void buttonClick(View view){

    }
}

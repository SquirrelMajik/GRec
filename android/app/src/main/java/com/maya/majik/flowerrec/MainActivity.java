package com.maya.majik.flowerrec;

import android.content.Context;
import android.content.CursorLoader;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.ImageView;

import java.io.File;
import java.util.Date;

public class MainActivity extends AppCompatActivity {


    String savePath = "sdcard/FlowerRec/images/";
    String tempFileName;//临时文件路径
    String tempPhotoPath;//选择照片或者或拍照完成后保存的照片地址
    private static final int PHOTO_REQUEST_CAMERA = 1;// 拍照
    private static final int PHOTO_REQUEST_GALLERY = 2;// 从相册中选择

    ImageView image;
    private Bitmap bitmap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        Button but_from_gallery = (Button) findViewById(R.id.but_from_gallery);
        Button but_take_a_pic = (Button) findViewById(R.id.but_take_a_pic);
        image = (ImageView) findViewById(R.id.image);

        if (but_take_a_pic != null) {
            but_take_a_pic.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    camera();
                }
            });
        }

        if (but_from_gallery != null) {
            but_from_gallery.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    gallery();
                }
            });
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    /**
     * 从相册获取
     */
    public void gallery() {
        // 激活系统图库，选择一张图片
        Intent intent = new Intent(Intent.ACTION_PICK);
        intent.setType("image/*");
        startActivityForResult(intent, PHOTO_REQUEST_GALLERY);
    }


    /*
     * 从拍照获取
     */
    public void camera() {
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        // 判断存储卡是否可以用，可用进行存储
        tempFileName = new Date().toString()+".png";
        if (hasSdcard()) {
            //设定拍照存放到自己指定的目录,可以先建好
            File file = new File(savePath);
            if(!file.exists()){
                file.mkdirs();
            }
            intent.putExtra(MediaStore.EXTRA_OUTPUT,
                    Uri.fromFile(new File(savePath, tempFileName)));
        }
        startActivityForResult(intent, PHOTO_REQUEST_CAMERA);
    }

    /**
     返回结果处理
     */
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {

        try {
            if (requestCode == PHOTO_REQUEST_GALLERY) {//相册
                if (data != null) {
                    // 得到图片的全路径
                    Uri uri = data.getData();
                    tempPhotoPath = getRealPathFromURI(uri, this);
                    //根据自己的需求写压缩图片的大小
                    bitmap= compressImageFromFile(tempPhotoPath, 400f, 400f);
                    image.setImageBitmap(bitmap);//显示图片
                }

            } else if (requestCode == PHOTO_REQUEST_CAMERA) {//照相
			/*
				1.好些设备在调用系统相机照相后返回的 data为null
				  解决办法就是在调用相机之前先设定好照片的路径和名称,拍完后直接拿来用
				2.如果图片地址没有图片存在,则表示没有进行照相
			*/
                tempPhotoPath = savePath + "/" + tempFileName;
                File file = new File(tempPhotoPath);
                if(file.isFile()){//判断是否有照相
                    bitmap= compressImageFromFile(tempPhotoPath,400f,400f);
                    image.setImageBitmap(bitmap);//显示图片
                }


            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    /**
     * 是否有sd卡
     * @return
     */
    public static boolean hasSdcard() {
        if (Environment.getExternalStorageState().equals(
                Environment.MEDIA_MOUNTED)) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * 获取uri的文件地址
     * @param contentUri
     * @param context
     * @return
     */
    public String getRealPathFromURI(Uri contentUri,Context context) {
        String[] proj = { MediaStore.Images.Media.DATA };
        CursorLoader loader = new CursorLoader(context, contentUri, proj, null, null, null);
        Cursor cursor = loader.loadInBackground();
        int column_index = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
        cursor.moveToFirst();
        return cursor.getString(column_index);
    }

    /**
     * 压缩图片减少内存使用
     * @param srcPath
     * @param hh
     * @param ww
     * @return
     */
    public static Bitmap compressImageFromFile(String srcPath, float hh, float ww) {
        BitmapFactory.Options newOpts = new BitmapFactory.Options();
        newOpts.inJustDecodeBounds = true;// 只读边,不读内容
        Bitmap bitmap = BitmapFactory.decodeFile(srcPath, newOpts);

        newOpts.inJustDecodeBounds = false;
        int w = newOpts.outWidth;
        int h = newOpts.outHeight;
        /*float hh = 300f;// 长
        float ww = 300f;//   高*/
        int be = 1;
        if (w > h && w > ww) {
            be = (int) (newOpts.outWidth / ww);
        } else if (w < h && h > hh) {
            be = (int) (newOpts.outHeight / hh);
        }
        if (be <= 0)
            be = 1;
        newOpts.inSampleSize = be;// 设置采样率
        newOpts.inPreferredConfig = Bitmap.Config.ARGB_8888;// 该模式是默认的,可不设
        newOpts.inPurgeable = true;// 同时设置才会有效
        newOpts.inInputShareable = true;// 当系统内存不够时候图片自动被回收
        bitmap = BitmapFactory.decodeFile(srcPath, newOpts);
        return bitmap;
    }

    /** 回收Bitmap的空间。 */
    public void recyleBitmap(Bitmap bitmap) {
        if (bitmap != null && !bitmap.isRecycled()) {
            bitmap.recycle();
            bitmap = null;
        }
    }
}

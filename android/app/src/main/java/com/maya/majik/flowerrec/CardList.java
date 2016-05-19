package com.maya.majik.flowerrec;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.JsonObject;
import com.koushikdutta.async.future.FutureCallback;
import com.koushikdutta.ion.Ion;

import java.io.File;
import java.util.ArrayList;
import java.util.Iterator;

import it.gmariotti.cardslib.library.internal.Card;
import it.gmariotti.cardslib.library.internal.CardArrayAdapter;
import it.gmariotti.cardslib.library.view.CardListView;


public class CardList extends FrameLayout {

    private ArrayList<Card> cards = new ArrayList<Card>();
    private CardArrayAdapter mCardArrayAdapter;
    private CardListView listView;
    private int MAXLENGTH = 10;

    public CardList(Context context, AttributeSet attrs) {
        super(context, attrs);
        LayoutInflater.from(context).inflate(R.layout.card_list, this);
        mCardArrayAdapter = new CardArrayAdapter(getContext() ,cards);

        listView = (CardListView) findViewById(R.id.card_list);

    }

    public Card getCard(String photoPath) {
        for (Card card : cards) {
            if (((MyCard)card).getPhotoPath().equals(photoPath)) {
                return card;
            }
        }
        return null;
    }

    /**
     * 添加 Card
     */
    public void addItem(String photoPath) {
        Card card = getCard(photoPath);
        if (card != null) {
            cards.remove(card);
            cards.add(0, card);
        } else {
            if (cards.size() >= MAXLENGTH){
                Toast.makeText(getContext(),
                        "10 records max",
                        Toast.LENGTH_LONG).show();
                cards.remove(MAXLENGTH - 1);
            }

            cards.add(0, new MyCard(getContext(), photoPath));
        }

        if (listView != null){
            listView.setAdapter(mCardArrayAdapter);
        }
    }



    //-------------------------------------------------------------------------------------------------------------
    // Cards
    //-------------------------------------------------------------------------------------------------------------


    /**
     * Card
     */
    public class MyCard extends Card {
        protected TextView content;
        protected ImageView image;
        protected ProgressBar progress;

        protected String photoPath;
        protected String result;

        /**
         * Constructor with a custom inner layout
         * @param context
         */
        public MyCard(Context context, String photoPath) {
            this(context, R.layout.card_main, photoPath);
        }

        /**
         *
         * @param context
         * @param innerLayout
         */
        public MyCard(Context context, int innerLayout, String photoPath) {
            super(context, innerLayout);
            init(photoPath);
        }

        /**
         * Init
         */
        private void init(String srcPath){
            photoPath = srcPath;
        }

        public String getPhotoPath() {
            return photoPath;
        }

        @Override
        public void setupInnerViewElements(ViewGroup parent, View view) {

            //Retrieve elements
            content = (TextView) parent.findViewById(R.id.card_content);
            image = (ImageView) parent.findViewById(R.id.card_image);
            progress = (ProgressBar) parent.findViewById(R.id.progress_bar);

            if(image != null) {
                Bitmap bitmap = compressImageFromFile(photoPath, 400f, 400f);
                image.setImageBitmap(bitmap);
            }

            if(progress != null && content != null){
                if(result != null) {
                    content.setText(result);
                    progress.setVisibility(View.GONE);
                } else {
                    content.setVisibility(View.GONE);
                    rec();
                }
            }
        }

        public void setContent(String string) {
            content.setText(string);
        }

        public Bitmap compressImageFromFile(String srcPath, float hh, float ww) {
            BitmapFactory.Options newOpts = new BitmapFactory.Options();
            newOpts.inJustDecodeBounds = true;// 只读边,不读内容
            Bitmap bitmap = BitmapFactory.decodeFile(srcPath, newOpts);
            System.out.print(bitmap);

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

        public void rec() {
            File input = new File(photoPath);
            Ion.with(getContext())
                    .load("http://10.0.2.2:6002")
                    .uploadProgressBar(progress)
                    .setMultipartFile("grec_file", "image/png", input)
                    .asJsonObject()
                    .setCallback(new FutureCallback<JsonObject>() {
                        @Override
                        public void onCompleted(Exception e, JsonObject data) {
                            // do stuff with the result or error
                            if(e == null && data != null && data.has("maybe")) {
                                result = data.get("maybe").getAsString();
                            } else {
                                result = "Sorry, it must be alien.";
                            }

                            content.setText(result);
                            progress.setVisibility(View.GONE);
                            content.setVisibility(View.VISIBLE);

                        }
                    });
        }

    }

}
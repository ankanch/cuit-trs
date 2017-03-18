package com.kanchsproject.teacherrating;

/**
 * Created by Kanch on 2015/7/7.
 *  kanchisme@gmail.com
 * 用来操作从Web API获取数据
 */
        import java.net.URL;
        import java.net.URLConnection;
        import java.io.BufferedReader;
        import java.io.IOException;
        import java.io.InputStreamReader;

public class WebClient{

    private static String _newLine = System.getProperty("line.separator");
    public WebClient()
    {    }
    public String getContent(String url, String oriEncoding, String targetEncoding) throws IOException
    {
        URL u = new URL(url);
        URLConnection uc = u.openConnection();
        BufferedReader in;

        if(oriEncoding == null || oriEncoding.length() == 0)
        {
            in = new BufferedReader(new InputStreamReader(uc.getInputStream()));
        }
        else
        {
            in = new BufferedReader(new InputStreamReader(uc.getInputStream(), oriEncoding));
        }
        String line;
        StringBuilder sb = new StringBuilder();
        while((line = in.readLine()) != null)
        {
            sb.append(line); sb.append(_newLine);
        }
        if(targetEncoding == null || targetEncoding.length() == 0)
        {
            return sb.toString();
        }
        return new String(sb.toString().getBytes(), targetEncoding);
    }
}


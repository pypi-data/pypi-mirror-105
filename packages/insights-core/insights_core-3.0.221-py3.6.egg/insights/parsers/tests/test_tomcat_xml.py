from insights.tests import context_wrap
from insights.parsers import tomcat_xml
from insights.parsers.tomcat_xml import TomcatWebXml
from insights.parsers.tomcat_xml import TomcatServerXml
import doctest

web_xml_content = """
<?xml version="1.0" encoding="ISO-8859-1"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<web-app xmlns="http://java.sun.com/xml/ns/javaee"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
    version="2.5">

  <!-- ======================== Introduction ============================== -->
  <!-- This document defines default values for *all* web applications      -->
  <!-- loaded into this instance of Tomcat.  As each application is         -->
  <!-- deployed, this file is processed, followed by the                    -->
  <!-- "/WEB-INF/web.xml" deployment descriptor from your own               -->
  <!-- applications.                                                        -->
  <!--                                                                      -->
  <!-- WARNING:  Do not configure application-specific resources here!      -->
  <!-- They should go in the "/WEB-INF/web.xml" file in your application.   -->


  <!-- ================== Built In Servlet Definitions ==================== -->


  <!-- The default servlet for all web applications, that serves static     -->
  <!-- resources.  It processes all requests that are not mapped to other   -->
  <!-- servlets with servlet mappings (defined either here or in your own   -->
  <!-- web.xml file.  This servlet supports the following initialization    -->
  <!-- parameters (default values are in square brackets):                  -->
  <!--                                                                      -->
  <!--   debug               Debugging detail level for messages logged     -->
  <!--                       by this servlet.  [0]                          -->
  <!--                                                                      -->
  <!--   fileEncoding        Encoding to be used to read static resources   -->
  <!--                       [platform default]                             -->
  <!--                                                                      -->
  <!--   input               Input buffer size (in bytes) when reading      -->
  <!--                       resources to be served.  [2048]                -->
  <!--                                                                      -->
  <!--   listings            Should directory listings be produced if there -->
  <!--                       is no welcome file in this directory?  [false] -->
  <!--                       WARNING: Listings for directories with many    -->
  <!--                       entries can be slow and may consume            -->
  <!--                       significant proportions of server resources.   -->
  <!--                                                                      -->
  <!--   output              Output buffer size (in bytes) when writing     -->
  <!--                       resources to be served.  [2048]                -->
  <!--                                                                      -->
  <!--   readonly            Is this context "read only", so HTTP           -->
  <!--                       commands like PUT and DELETE are               -->
  <!--                       rejected?  [true]                              -->
  <!--                                                                      -->
  <!--   readmeFile          File name to display with the directory        -->
  <!--                       contents. [null]                               -->
  <!--                                                                      -->
  <!--   sendfileSize        If the connector used supports sendfile, this  -->
  <!--                       represents the minimal file size in KB for     -->
  <!--                       which sendfile will be used. Use a negative    -->
  <!--                       value to always disable sendfile.  [48]        -->
  <!--                                                                      -->
  <!--   useAcceptRanges     Should the Accept-Ranges header be included    -->
  <!--                       in responses where appropriate? [true]         -->
  <!--                                                                      -->
  <!--  For directory listing customization. Checks localXsltFile, then     -->
  <!--  globalXsltFile, then defaults to original behavior.                 -->
  <!--                                                                      -->
  <!--   localXsltFile       Make directory listings an XML doc and         -->
  <!--                       pass the result to this style sheet residing   -->
  <!--                       in that directory. This overrides              -->
  <!--                        globalXsltFile[null]                          -->
  <!--                                                                      -->
  <!--   globalXsltFile      Site wide configuration version of             -->
  <!--                       localXsltFile. This argument must either       -->
  <!--                        an aboslute or relative ( to either           -->
  <!--                        CATALINA_BASE/conf or CATALINA_HOME/conf     -->
  <!--                        path that points to the location below       -->
  <!--                        CATALINA_BASE/conf (checked first) or        -->
  <!--                        $CATLINA_HOME/conf (checked second).         -->
  <!--                                                                      -->
  <!--                                                                      -->

    <servlet>
        <servlet-name>default</servlet-name>
        <servlet-class>org.apache.catalina.servlets.DefaultServlet</servlet-class>
        <init-param>
            <param-name>debug</param-name>
            <param-value>0</param-value>
        </init-param>
        <init-param>
            <param-name>listings</param-name>
            <param-value>false</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>


  <!-- This servlet has been deprecated due to security concerns. Servlets  -->
  <!-- should be explicitly mapped in web.xml                               -->
  <!--                                                                      -->
  <!-- The "invoker" servlet, which executes anonymous servlet classes      -->
  <!-- that have not been defined in a web.xml file.  Traditionally, this   -->
  <!-- servlet is mapped to the URL pattern "/servlet/*", but you can map   -->
  <!-- it to other patterns as well.  The extra path info portion of such a -->
  <!-- request must be the fully qualified class name of a Java class that  -->
  <!-- implements Servlet (or extends HttpServlet), or the servlet name     -->
  <!-- of an existing servlet definition.     This servlet supports the     -->
  <!-- following initialization parameters (default values are in square    -->
  <!-- brackets):                                                           -->
  <!--                                                                      -->
  <!--   debug               Debugging detail level for messages logged     -->
  <!--                       by this servlet.  [0]                          -->

<!--
    <servlet>
        <servlet-name>invoker</servlet-name>
        <servlet-class>
          org.apache.catalina.servlets.InvokerServlet
        </servlet-class>
        <init-param>
            <param-name>debug</param-name>
            <param-value>0</param-value>
        </init-param>
        <load-on-startup>2</load-on-startup>
    </servlet>
-->


  <!-- The JSP page compiler and execution servlet, which is the mechanism  -->
  <!-- used by Tomcat to support JSP pages.  Traditionally, this servlet    -->
  <!-- is mapped to the URL pattern "*.jsp".  This servlet supports the     -->
  <!-- following initialization parameters (default values are in square    -->
  <!-- brackets):                                                           -->
  <!--                                                                      -->
  <!--   checkInterval       If development is false and checkInterval is   -->
  <!--                       greater than zero, background compilations are -->
  <!--                       enabled. checkInterval is the time in seconds  -->
  <!--                       between checks to see if a JSP page (and its   -->
  <!--                       dependent files) needs to  be recompiled. [0]  -->
  <!--                                                                      -->
  <!--   classdebuginfo      Should the class file be compiled with         -->
  <!--                       debugging information?  [true]                 -->
  <!--                                                                      -->
  <!--   classpath           What class path should I use while compiling   -->
  <!--                       generated servlets?  [Created dynamically      -->
  <!--                       based on the current web application]          -->
  <!--                                                                      -->
  <!--   compiler            Which compiler Ant should use to compile JSP   -->
  <!--                       pages.  See the jasper documentation for more  -->
  <!--                       information.                                   -->
  <!--                                                                      -->
  <!--   compilerSourceVM    Compiler source VM. [1.5]                      -->
  <!--                                                                      -->
  <!--   compilerTargetVM    Compiler target VM. [1.5]                      -->
  <!--                                                                      -->
  <!--   development         Is Jasper used in development mode? If true,   -->
  <!--                       the frequency at which JSPs are checked for    -->
  <!--                       modification may be specified via the          -->
  <!--                       modificationTestInterval parameter. [true]     -->
  <!--                                                                      -->
  <!--   displaySourceFragment                                              -->
  <!--                       Should a source fragment be included in        -->
  <!--                       exception messages? [true]                     -->
  <!--                                                                      -->
  <!--   dumpSmap            Should the SMAP info for JSR45 debugging be    -->
  <!--                       dumped to a file? [false]                      -->
  <!--                       False if suppressSmap is true                  -->
  <!--                                                                      -->
  <!--   enablePooling       Determines whether tag handler pooling is      -->
  <!--                       enabled. This is a compilation option. It will -->
  <!--                       not alter the behaviour of JSPs that have      -->
  <!--                       already been compiled. [true]                  -->
  <!--                                                                      -->
  <!--   engineOptionsClass  Allows specifying the Options class used to    -->
  <!--                       configure Jasper. If not present, the default  -->
  <!--                       EmbeddedServletOptions will be used.           -->
  <!--                                                                      -->
  <!--   errorOnUseBeanInvalidClassAttribute                                -->
  <!--                       Should Jasper issue an error when the value of -->
  <!--                       the class attribute in an useBean action is    -->
  <!--                       not a valid bean class?  [true]                -->
  <!--                                                                      -->
  <!--   fork                Tell Ant to fork compiles of JSP pages so that -->
  <!--                       a separate JVM is used for JSP page compiles   -->
  <!--                       from the one Tomcat is running in. [true]      -->
  <!--                                                                      -->
  <!--   genStrAsCharArray   Should text strings be generated as char       -->
  <!--                       arrays, to improve performance in some cases?  -->
  <!--                       [false]                                        -->
  <!--                                                                      -->
  <!--   ieClassId           The class-id value to be sent to Internet      -->
  <!--                       Explorer when using <jsp:plugin> tags.         -->
  <!--                       [clsid:8AD9C840-044E-11D1-B3E9-00805F499D93]   -->
  <!--                                                                      -->
  <!--   javaEncoding        Java file encoding to use for generating java  -->
  <!--                       source files. [UTF8]                           -->
  <!--                                                                      -->
  <!--   keepgenerated       Should we keep the generated Java source code  -->
  <!--                       for each page instead of deleting it? [true]   -->
  <!--                                                                      -->
  <!--   mappedfile          Should we generate static content with one     -->
  <!--                       print statement per input line, to ease        -->
  <!--                       debugging?  [true]                             -->
  <!--                                                                      -->
  <!--   modificationTestInterval                                           -->
  <!--                       Causes a JSP (and its dependent files) to not  -->
  <!--                       be checked for modification during the         -->
  <!--                       specified time interval (in seconds) from the  -->
  <!--                       last time the JSP was checked for              -->
  <!--                       modification. A value of 0 will cause the JSP  -->
  <!--                       to be checked on every access.                 -->
  <!--                       Used in development mode only. [4]             -->
  <!--                                                                      -->
  <!--   scratchdir          What scratch directory should we use when      -->
  <!--                       compiling JSP pages?  [default work directory  -->
  <!--                       for the current web application]               -->
  <!--                                                                      -->
  <!--   suppressSmap        Should the generation of SMAP info for JSR45   -->
  <!--                       debugging be suppressed?  [false]              -->
  <!--                                                                      -->
  <!--   trimSpaces          Should white spaces in template text between   -->
  <!--                       actions or directives be trimmed?  [false]     -->
  <!--                                                                      -->
  <!--   xpoweredBy          Determines whether X-Powered-By response       -->
  <!--                       header is added by generated servlet  [false]  -->
  <!--                                                                      -->
  <!-- If you wish to use Jikes to compile JSP pages:                       -->
  <!--   Please see the "Using Jikes" section of the Jasper-HowTo           -->
  <!--   page in the Tomcat documentation.                                  -->

    <servlet>
        <servlet-name>jsp</servlet-name>
        <servlet-class>org.apache.jasper.servlet.JspServlet</servlet-class>
        <init-param>
            <param-name>fork</param-name>
            <param-value>false</param-value>
        </init-param>
        <init-param>
            <param-name>xpoweredBy</param-name>
            <param-value>false</param-value>
        </init-param>
        <init-param>
            <param-name>development</param-name>
            <param-value>false</param-value>
        </init-param>
        <load-on-startup>3</load-on-startup>
    </servlet>


  <!-- NOTE: An SSI Filter is also available as an alternative SSI          -->
  <!-- implementation. Use either the Servlet or the Filter but NOT both.   -->
  <!--                                                                      -->
  <!-- Server Side Includes processing servlet, which processes SSI         -->
  <!-- directives in HTML pages consistent with similar support in web      -->
  <!-- servers like Apache.  Traditionally, this servlet is mapped to the   -->
  <!-- URL pattern "*.shtml".  This servlet supports the following          -->
  <!-- initialization parameters (default values are in square brackets):   -->
  <!--                                                                      -->
  <!--   buffered            Should output from this servlet be buffered?   -->
  <!--                       (0=false, 1=true)  [0]                         -->
  <!--                                                                      -->
  <!--   debug               Debugging detail level for messages logged     -->
  <!--                       by this servlet.  [0]                          -->
  <!--                                                                      -->
  <!--   expires             The number of seconds before a page with SSI   -->
  <!--                       directives will expire.  [No default]          -->
  <!--                                                                      -->
  <!--   isVirtualWebappRelative                                            -->
  <!--                       Should "virtual" paths be interpreted as       -->
  <!--                       relative to the context root, instead of       -->
  <!--                       the server root?  (0=false, 1=true) [0]        -->
  <!--                                                                      -->
  <!--   inputEncoding       The encoding to assume for SSI resources if    -->
  <!--                       one is not available from the resource.        -->
  <!--                       [Platform default]                             -->
  <!--                                                                      -->
  <!--   outputEncoding      The encoding to use for the page that results  -->
  <!--                       from the SSI processing. [UTF-8]               -->

<!--
    <servlet>
        <servlet-name>ssi</servlet-name>
        <servlet-class>
          org.apache.catalina.ssi.SSIServlet
        </servlet-class>
        <init-param>
          <param-name>buffered</param-name>
          <param-value>1</param-value>
        </init-param>
        <init-param>
          <param-name>debug</param-name>
          <param-value>0</param-value>
        </init-param>
        <init-param>
          <param-name>expires</param-name>
          <param-value>666</param-value>
        </init-param>
        <init-param>
          <param-name>isVirtualWebappRelative</param-name>
          <param-value>0</param-value>
        </init-param>
        <load-on-startup>4</load-on-startup>
    </servlet>
-->


  <!-- Common Gateway Includes (CGI) processing servlet, which supports     -->
  <!-- execution of external applications that conform to the CGI spec      -->
  <!-- requirements.  Typically, this servlet is mapped to the URL pattern  -->
  <!-- "/cgi-bin/*", which means that any CGI applications that are         -->
  <!-- executed must be present within the web application.  This servlet   -->
  <!-- supports the following initialization parameters (default values     -->
  <!-- are in square brackets):                                             -->
  <!--                                                                      -->
  <!--   cgiPathPrefix        The CGI search path will start at             -->
  <!--                        webAppRootDir + File.separator + this prefix. -->
  <!--                        [WEB-INF/cgi]                                 -->
  <!--                                                                      -->
  <!--   debug                Debugging detail level for messages logged    -->
  <!--                        by this servlet.  [0]                         -->
  <!--                                                                      -->
  <!--   executable           Name of the executable used to run the        -->
  <!--                        script. [perl]                                -->
  <!--                                                                      -->
  <!--   parameterEncoding    Name of parameter encoding to be used with    -->
  <!--                        CGI servlet.                                  -->
  <!--                        [System.getProperty("file.encoding","UTF-8")] -->
  <!--                                                                      -->
  <!--   passShellEnvironment Should the shell environment variables (if    -->
  <!--                        any) be passed to the CGI script? [false]     -->
  <!--                                                                      -->
  <!--   stderrTimeout        The time (in milliseconds) to wait for the    -->
  <!--                        reading of stderr to complete before          -->
  <!--                        terminating the CGI process. [2000]           -->

<!--
    <servlet>
        <servlet-name>cgi</servlet-name>
        <servlet-class>org.apache.catalina.servlets.CGIServlet</servlet-class>
        <init-param>
          <param-name>debug</param-name>
          <param-value>0</param-value>
        </init-param>
        <init-param>
          <param-name>cgiPathPrefix</param-name>
          <param-value>WEB-INF/cgi</param-value>
        </init-param>
         <load-on-startup>5</load-on-startup>
    </servlet>
-->


  <!-- ================ Built In Servlet Mappings ========================= -->


  <!-- The servlet mappings for the built in servlets defined above.  Note  -->
  <!-- that, by default, the CGI and SSI servlets are *not* mapped.  You    -->
  <!-- must uncomment these mappings (or add them to your application's own -->
  <!-- web.xml deployment descriptor) to enable these services              -->

    <!-- The mapping for the default servlet -->
    <servlet-mapping>
        <servlet-name>default</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>

    <!-- The mapping for the deprecated invoker servlet -->
<!--
    <servlet-mapping>
        <servlet-name>invoker</servlet-name>
        <url-pattern>/servlet/*</url-pattern>
    </servlet-mapping>
-->

    <!-- The mapping for the JSP servlet -->
    <servlet-mapping>
        <servlet-name>jsp</servlet-name>
        <url-pattern>*.jsp</url-pattern>
    </servlet-mapping>

    <servlet-mapping>
        <servlet-name>jsp</servlet-name>
        <url-pattern>*.jspx</url-pattern>
    </servlet-mapping>

    <!-- The mapping for the SSI servlet -->
<!--
    <servlet-mapping>
        <servlet-name>ssi</servlet-name>
        <url-pattern>*.shtml</url-pattern>
    </servlet-mapping>
-->

    <!-- The mapping for the CGI Gateway servlet -->

<!--
    <servlet-mapping>
        <servlet-name>cgi</servlet-name>
        <url-pattern>/cgi-bin/*</url-pattern>
    </servlet-mapping>
-->


  <!-- ================== Built In Filter Definitions ===================== -->

  <!-- NOTE: An SSI Servlet is also available as an alternative SSI         -->
  <!-- implementation. Use either the Servlet or the Filter but NOT both.   -->
  <!--                                                                      -->
  <!-- Server Side Includes processing filter, which processes SSI          -->
  <!-- directives in HTML pages consistent with similar support in web      -->
  <!-- servers like Apache.  Traditionally, this filter is mapped to the    -->
  <!-- URL pattern "*.shtml", though it can be mapped to "*" as it will     -->
  <!-- selectively enable/disable SSI processing based on mime types. For   -->
  <!-- this to work you will need to uncomment the .shtml mime type         -->
  <!-- definition towards the bottom of this file.                          -->
  <!-- The contentType init param allows you to apply SSI processing to JSP -->
  <!-- pages, javascript, or any other content you wish.  This filter       -->
  <!-- supports the following initialization parameters (default values are -->
  <!-- in square brackets):                                                 -->
  <!--                                                                      -->
  <!--   contentType         A regex pattern that must be matched before    -->
  <!--                       SSI processing is applied.                     -->
  <!--                       [text/x-server-parsed-html(;.*)?]              -->
  <!--                                                                      -->
  <!--   debug               Debugging detail level for messages logged     -->
  <!--                       by this servlet.  [0]                          -->
  <!--                                                                      -->
  <!--   expires             The number of seconds before a page with SSI   -->
  <!--                       directives will expire.  [No default]          -->
  <!--                                                                      -->
  <!--   isVirtualWebappRelative                                            -->
  <!--                       Should "virtual" paths be interpreted as       -->
  <!--                       relative to the context root, instead of       -->
  <!--                       the server root?  (0=false, 1=true) [0]        -->

<!--
    <filter>
        <filter-name>ssi</filter-name>
        <filter-class>
          org.apache.catalina.ssi.SSIFilter
        </filter-class>
        <init-param>
          <param-name>contentType</param-name>
          <param-value>text/x-server-parsed-html(;.*)?</param-value>
        </init-param>
        <init-param>
          <param-name>debug</param-name>
          <param-value>0</param-value>
        </init-param>
        <init-param>
          <param-name>expires</param-name>
          <param-value>666</param-value>
        </init-param>
        <init-param>
          <param-name>isVirtualWebappRelative</param-name>
          <param-value>0</param-value>
        </init-param>
    </filter>
-->


  <!-- ==================== Built In Filter Mappings ====================== -->

  <!-- The mapping for the SSI Filter -->
<!--
    <filter-mapping>
        <filter-name>ssi</filter-name>
        <url-pattern>*.shtml</url-pattern>
    </filter-mapping>
-->


  <!-- ==================== Default Session Configuration ================= -->
  <!-- You can set the default session timeout (in minutes) for all newly   -->
  <!-- created sessions by modifying the value below.                       -->

    <session-config>
        <session-timeout>30</session-timeout>
    </session-config>


  <!-- ===================== Default MIME Type Mappings =================== -->
  <!-- When serving static resources, Tomcat will automatically generate    -->
  <!-- a "Content-Type" header based on the resource's filename extension,  -->
  <!-- based on these mappings.  Additional mappings can be added here (to  -->
  <!-- apply to all web applications), or in your own application's web.xml -->
  <!-- deployment descriptor.                                               -->

    <mime-mapping>
        <extension>abs</extension>
        <mime-type>audio/x-mpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>ai</extension>
        <mime-type>application/postscript</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>aif</extension>
        <mime-type>audio/x-aiff</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>aifc</extension>
        <mime-type>audio/x-aiff</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>aiff</extension>
        <mime-type>audio/x-aiff</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>aim</extension>
        <mime-type>application/x-aim</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>art</extension>
        <mime-type>image/x-jg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>asf</extension>
        <mime-type>video/x-ms-asf</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>asx</extension>
        <mime-type>video/x-ms-asf</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>au</extension>
        <mime-type>audio/basic</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>avi</extension>
        <mime-type>video/x-msvideo</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>avx</extension>
        <mime-type>video/x-rad-screenplay</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>bcpio</extension>
        <mime-type>application/x-bcpio</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>bin</extension>
        <mime-type>application/octet-stream</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>bmp</extension>
        <mime-type>image/bmp</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>body</extension>
        <mime-type>text/html</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>cdf</extension>
        <mime-type>application/x-cdf</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>cer</extension>
        <mime-type>application/x-x509-ca-cert</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>class</extension>
        <mime-type>application/java</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>cpio</extension>
        <mime-type>application/x-cpio</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>csh</extension>
        <mime-type>application/x-csh</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>css</extension>
        <mime-type>text/css</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>dib</extension>
        <mime-type>image/bmp</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>doc</extension>
        <mime-type>application/msword</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>dtd</extension>
        <mime-type>application/xml-dtd</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>dv</extension>
        <mime-type>video/x-dv</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>dvi</extension>
        <mime-type>application/x-dvi</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>eps</extension>
        <mime-type>application/postscript</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>etx</extension>
        <mime-type>text/x-setext</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>exe</extension>
        <mime-type>application/octet-stream</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>gif</extension>
        <mime-type>image/gif</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>gtar</extension>
        <mime-type>application/x-gtar</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>gz</extension>
        <mime-type>application/x-gzip</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>hdf</extension>
        <mime-type>application/x-hdf</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>hqx</extension>
        <mime-type>application/mac-binhex40</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>htc</extension>
        <mime-type>text/x-component</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>htm</extension>
        <mime-type>text/html</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>html</extension>
        <mime-type>text/html</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>hqx</extension>
        <mime-type>application/mac-binhex40</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>ief</extension>
        <mime-type>image/ief</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>jad</extension>
        <mime-type>text/vnd.sun.j2me.app-descriptor</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>jar</extension>
        <mime-type>application/java-archive</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>java</extension>
        <mime-type>text/plain</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>jnlp</extension>
        <mime-type>application/x-java-jnlp-file</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>jpe</extension>
        <mime-type>image/jpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>jpeg</extension>
        <mime-type>image/jpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>jpg</extension>
        <mime-type>image/jpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>js</extension>
        <mime-type>text/javascript</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>jsf</extension>
        <mime-type>text/plain</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>jspf</extension>
        <mime-type>text/plain</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>kar</extension>
        <mime-type>audio/x-midi</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>latex</extension>
        <mime-type>application/x-latex</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>m3u</extension>
        <mime-type>audio/x-mpegurl</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mac</extension>
        <mime-type>image/x-macpaint</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>man</extension>
        <mime-type>application/x-troff-man</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mathml</extension>
        <mime-type>application/mathml+xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>me</extension>
        <mime-type>application/x-troff-me</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mid</extension>
        <mime-type>audio/x-midi</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>midi</extension>
        <mime-type>audio/x-midi</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mif</extension>
        <mime-type>application/x-mif</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mov</extension>
        <mime-type>video/quicktime</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>movie</extension>
        <mime-type>video/x-sgi-movie</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mp1</extension>
        <mime-type>audio/x-mpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mp2</extension>
        <mime-type>audio/x-mpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mp3</extension>
        <mime-type>audio/x-mpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mp4</extension>
        <mime-type>video/mp4</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mpa</extension>
        <mime-type>audio/x-mpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mpe</extension>
        <mime-type>video/mpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mpeg</extension>
        <mime-type>video/mpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mpega</extension>
        <mime-type>audio/x-mpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mpg</extension>
        <mime-type>video/mpeg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>mpv2</extension>
        <mime-type>video/mpeg2</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>ms</extension>
        <mime-type>application/x-wais-source</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>nc</extension>
        <mime-type>application/x-netcdf</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>oda</extension>
        <mime-type>application/oda</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Database -->
        <extension>odb</extension>
        <mime-type>application/vnd.oasis.opendocument.database</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Chart -->
        <extension>odc</extension>
        <mime-type>application/vnd.oasis.opendocument.chart</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Formula -->
        <extension>odf</extension>
        <mime-type>application/vnd.oasis.opendocument.formula</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Drawing -->
        <extension>odg</extension>
        <mime-type>application/vnd.oasis.opendocument.graphics</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Image -->
        <extension>odi</extension>
        <mime-type>application/vnd.oasis.opendocument.image</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Master Document -->
        <extension>odm</extension>
        <mime-type>application/vnd.oasis.opendocument.text-master</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Presentation -->
        <extension>odp</extension>
        <mime-type>application/vnd.oasis.opendocument.presentation</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Spreadsheet -->
        <extension>ods</extension>
        <mime-type>application/vnd.oasis.opendocument.spreadsheet</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Text -->
        <extension>odt</extension>
        <mime-type>application/vnd.oasis.opendocument.text</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>ogg</extension>
        <mime-type>application/ogg</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Drawing Template -->
        <extension>otg </extension>
        <mime-type>application/vnd.oasis.opendocument.graphics-template</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- HTML Document Template -->
        <extension>oth</extension>
        <mime-type>application/vnd.oasis.opendocument.text-web</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Presentation Template -->
        <extension>otp</extension>
        <mime-type>application/vnd.oasis.opendocument.presentation-template</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Spreadsheet Template -->
        <extension>ots</extension>
        <mime-type>application/vnd.oasis.opendocument.spreadsheet-template </mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- OpenDocument Text Template -->
        <extension>ott</extension>
        <mime-type>application/vnd.oasis.opendocument.text-template</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>pbm</extension>
        <mime-type>image/x-portable-bitmap</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>pct</extension>
        <mime-type>image/pict</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>pdf</extension>
        <mime-type>application/pdf</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>pgm</extension>
        <mime-type>image/x-portable-graymap</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>pic</extension>
        <mime-type>image/pict</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>pict</extension>
        <mime-type>image/pict</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>pls</extension>
        <mime-type>audio/x-scpls</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>png</extension>
        <mime-type>image/png</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>pnm</extension>
        <mime-type>image/x-portable-anymap</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>pnt</extension>
        <mime-type>image/x-macpaint</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>ppm</extension>
        <mime-type>image/x-portable-pixmap</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>ppt</extension>
        <mime-type>application/vnd.ms-powerpoint</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>pps</extension>
        <mime-type>application/vnd.ms-powerpoint</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>ps</extension>
        <mime-type>application/postscript</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>psd</extension>
        <mime-type>image/x-photoshop</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>qt</extension>
        <mime-type>video/quicktime</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>qti</extension>
        <mime-type>image/x-quicktime</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>qtif</extension>
        <mime-type>image/x-quicktime</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>ras</extension>
        <mime-type>image/x-cmu-raster</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>rdf</extension>
        <mime-type>application/rdf+xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>rgb</extension>
        <mime-type>image/x-rgb</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>rm</extension>
        <mime-type>application/vnd.rn-realmedia</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>roff</extension>
        <mime-type>application/x-troff</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>rtf</extension>
        <mime-type>application/rtf</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>rtx</extension>
        <mime-type>text/richtext</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>sh</extension>
        <mime-type>application/x-sh</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>shar</extension>
        <mime-type>application/x-shar</mime-type>
    </mime-mapping>
<!--
    <mime-mapping>
        <extension>shtml</extension>
        <mime-type>text/x-server-parsed-html</mime-type>
    </mime-mapping>
-->
    <mime-mapping>
        <extension>smf</extension>
        <mime-type>audio/x-midi</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>sit</extension>
        <mime-type>application/x-stuffit</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>snd</extension>
        <mime-type>audio/basic</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>src</extension>
        <mime-type>application/x-wais-source</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>sv4cpio</extension>
        <mime-type>application/x-sv4cpio</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>sv4crc</extension>
        <mime-type>application/x-sv4crc</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>svg</extension>
        <mime-type>image/svg+xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>svgz</extension>
        <mime-type>image/svg+xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>swf</extension>
        <mime-type>application/x-shockwave-flash</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>t</extension>
        <mime-type>application/x-troff</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>tar</extension>
        <mime-type>application/x-tar</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>tcl</extension>
        <mime-type>application/x-tcl</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>tex</extension>
        <mime-type>application/x-tex</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>texi</extension>
        <mime-type>application/x-texinfo</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>texinfo</extension>
        <mime-type>application/x-texinfo</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>tif</extension>
        <mime-type>image/tiff</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>tiff</extension>
        <mime-type>image/tiff</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>tr</extension>
        <mime-type>application/x-troff</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>tsv</extension>
        <mime-type>text/tab-separated-values</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>txt</extension>
        <mime-type>text/plain</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>ulw</extension>
        <mime-type>audio/basic</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>ustar</extension>
        <mime-type>application/x-ustar</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>vxml</extension>
        <mime-type>application/voicexml+xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>xbm</extension>
        <mime-type>image/x-xbitmap</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>xht</extension>
        <mime-type>application/xhtml+xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>xhtml</extension>
        <mime-type>application/xhtml+xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>xls</extension>
        <mime-type>application/vnd.ms-excel</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>xml</extension>
        <mime-type>application/xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>xpm</extension>
        <mime-type>image/x-xpixmap</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>xsl</extension>
        <mime-type>application/xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>xslt</extension>
        <mime-type>application/xslt+xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>xul</extension>
        <mime-type>application/vnd.mozilla.xul+xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>xwd</extension>
        <mime-type>image/x-xwindowdump</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>vsd</extension>
        <mime-type>application/x-visio</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>wav</extension>
        <mime-type>audio/x-wav</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- Wireless Bitmap -->
        <extension>wbmp</extension>
        <mime-type>image/vnd.wap.wbmp</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- WML Source -->
        <extension>wml</extension>
        <mime-type>text/vnd.wap.wml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- Compiled WML -->
        <extension>wmlc</extension>
        <mime-type>application/vnd.wap.wmlc</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- WML Script Source -->
        <extension>wmls</extension>
        <mime-type>text/vnd.wap.wmlscript</mime-type>
    </mime-mapping>
    <mime-mapping>
        <!-- Compiled WML Script -->
        <extension>wmlscriptc</extension>
        <mime-type>application/vnd.wap.wmlscriptc</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>wmv</extension>
        <mime-type>video/x-ms-wmv</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>wrl</extension>
        <mime-type>x-world/x-vrml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>wspolicy</extension>
        <mime-type>application/wspolicy+xml</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>Z</extension>
        <mime-type>application/x-compress</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>z</extension>
        <mime-type>application/x-compress</mime-type>
    </mime-mapping>
    <mime-mapping>
        <extension>zip</extension>
        <mime-type>application/zip</mime-type>
    </mime-mapping>

  <!-- ==================== Default Welcome File List ===================== -->
  <!-- When a request URI refers to a directory, the default servlet looks  -->
  <!-- for a "welcome file" within that directory and, if present,          -->
  <!-- to the corresponding resource URI for display.  If no welcome file   -->
  <!-- is present, the default servlet either serves a directory listing,   -->
  <!-- or returns a 404 status, depending on how it is configured.          -->
  <!--                                                                      -->
  <!-- If you define welcome files in your own application's web.xml        -->
  <!-- deployment descriptor, that list *replaces* the list configured      -->
  <!-- here, so be sure that you include any of the default values that     -->
  <!-- you wish to include.                                                 -->

    <welcome-file-list>
        <welcome-file>index.html</welcome-file>
        <welcome-file>index.htm</welcome-file>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>

</web-app>
""".strip()

web_xml_content_missing_timeout = """
<?xml version="1.0" encoding="ISO-8859-1"?>
<web-app xmlns="http://java.sun.com/xml/ns/javaee"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
    version="2.5">

    <servlet>
        <servlet-name>default</servlet-name>
        <servlet-class>org.apache.catalina.servlets.DefaultServlet</servlet-class>
        <init-param>
            <param-name>debug</param-name>
            <param-value>0</param-value>
        </init-param>
        <init-param>
            <param-name>listings</param-name>
            <param-value>false</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
</web-app>
"""


def test_get_tmo():
    result = TomcatWebXml(context_wrap(web_xml_content))
    assert result.get("session-timeout") == 30


def test_get_tmo_missing_timeout():
    result = TomcatWebXml(context_wrap(web_xml_content_missing_timeout))
    assert result.get("session-timeout") is None


server_xml_content = """
<?xml version='1.0' encoding='utf-8'?>
<Server port="8005" shutdown="SHUTDOWN">

  <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on" />
  <Listener className="org.apache.catalina.core.JasperListener" />
  <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener" />
  <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener" />
<Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener" />
  <GlobalNamingResources>
    <Resource name="UserDatabase" auth="Container"
              type="org.apache.catalina.UserDatabase"
              description="User database that can be updated and saved"
              factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
              pathname="conf/tomcat-users.xml" />
  </GlobalNamingResources>

  <!-- A "Service" is a collection of one or more "Connectors" that share
       a single "Container" Note:  A "Service" is not itself a "Container",
       so you may not define subcomponents such as "Valves" at this level.
       Documentation at /docs/config/service.html
   -->
  <Service name="Catalina">
    <Connector port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" />

    <Connector port="8443" protocol="HTTP/1.1" SSLEnabled="true"
               maxThreads="150" scheme="https" secure="true"
               clientAuth="want"
               sslProtocols="TLSv1.2,TLSv1.1,TLSv1"
               keystoreFile="conf/keystore"
               truststoreFile="conf/keystore"
               keystorePass="oXQ8LfAGsf97KQxwwPta2X3vnUv7P5QM"
               keystoreType="PKCS12"
               ciphers="SSL_RSA_WITH_3DES_EDE_CBC_SHA,
                    TLS_RSA_WITH_AES_256_CBC_SHA,
                    TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA,
                    TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA,
                    TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA,
                    TLS_ECDH_RSA_WITH_AES_128_CBC_SHA,
                    TLS_ECDH_RSA_WITH_AES_256_CBC_SHA,
                    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA"
               truststorePass="oXQ8LfAGsf97KQxwwPta2X3vnUv7P5QM" />

    <!-- Define an AJP 1.3 Connector on port 8009 -->
    <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />


    <Engine name="Catalina" defaultHost="localhost">

      <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
             resourceName="UserDatabase"/>

      <Host name="localhost"  appBase="webapps"
            unpackWARs="true" autoDeploy="true"
            xmlValidation="false" xmlNamespaceAware="false">

      </Host>
    </Engine>
  </Service>
</Server>
"""


def test_tomcat_server_xml():
    result = TomcatServerXml(context_wrap(server_xml_content))
    engines = result.get_elements(".//Service/Engine")
    assert len(engines) == 1
    assert engines[0].get('name') == "Catalina"


def test_web_xml_doc_examples():
    env = {
            'TomcatWebXml': TomcatWebXml,
            'web_xml': TomcatWebXml(context_wrap(web_xml_content, path='/usr/share/tomcat/web.xml')),
            'TomcatServerXml': TomcatServerXml,
            'server_xml': TomcatServerXml(context_wrap(server_xml_content, path='/usr/share/tomcat/server.xml'))
          }
    failed, total = doctest.testmod(tomcat_xml, globs=env)
    assert failed == 0

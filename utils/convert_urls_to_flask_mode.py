import os
import shutil

files = [
    "./vendors/jquery/dist/jquery.min.js",
    "./vendors/bootstrap/dist/js/bootstrap.bundle.min.js",
    "./vendors/fastclick/lib/fastclick.js",
    "./vendors/nprogress/nprogress.js",
    "./vendors/Chart.js/dist/Chart.min.js",
    "./vendors/gauge.js/dist/gauge.min.js",
    "./vendors/bootstrap-progressbar/bootstrap-progressbar.min.js",
    "./vendors/iCheck/icheck.min.js",
    "./vendors/skycons/skycons.js",
    "./vendors/Flot/jquery.flot.js",
    "./vendors/Flot/jquery.flot.pie.js",
    "./vendors/Flot/jquery.flot.time.js",
    "./vendors/Flot/jquery.flot.stack.js",
    "./vendors/Flot/jquery.flot.resize.js",
    "./vendors/flot.orderbars/js/jquery.flot.orderBars.js",
    "./vendors/flot-spline/js/jquery.flot.spline.min.js",
    "./vendors/flot.curvedlines/curvedLines.js",
    "./vendors/DateJS/build/date.js",
    "./vendors/jqvmap/dist/jquery.vmap.js",
    "./vendors/jqvmap/dist/maps/jquery.vmap.world.js",
    "./vendors/jqvmap/examples/js/jquery.vmap.sampledata.js",
    "./vendors/moment/min/moment.min.js",
    "./vendors/bootstrap-daterangepicker/daterangepicker.js"
    ]



with open("static_urls.txt", "w") as f:
    for fid in files:
        shutil.copy(fid, os.path.join("static", "js", os.path.basename(fid)))
        line = '<script type=text/javascript src="{{url_for(' + '\'static\'' + ', filename=' + '\'js/{}\''.format(os.path.basename(fid)) + ') }}"></script>\n'
        f.write(line)

files = [
    "./vendors/bootstrap/dist/css/bootstrap.min.css",
    "./vendors/font-awesome/css/font-awesome.min.css",
    "./vendors/nprogress/nprogress.css",
    "./build/css/custom.min.css"
    ]

with open("static_urls.txt", "a") as f:
    for fid in files:
        shutil.copy(fid, os.path.join("static", "css", os.path.basename(fid)))
        line = '<script type=text/javascript src="{{url_for(' + '\'static\'' + ', filename=' + '\'css/{}\''.format(os.path.basename(fid)) + ') }}"></script>\n'
        f.write(line)    
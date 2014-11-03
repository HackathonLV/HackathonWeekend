/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

/* Code to pull a list from XML


$("#sample-page").live('pagebeforecreate', function() {
     $.get('http://ontariosheep.org/mobile/data/data_olex.php',function(data){
            $('#list').empty();
            $(data).find('item').each(function(){
                var $item = $(this);
                var html = '';
                html += '<li> <a href="#demo-mail"><h3>' + $item.attr('name') + '</h3>';
                html += '<img src="img/'+ $item.attr('image') +'" class="ui-li-thumb" />';
                html += '<p class="ui-li-aside"><strong>$' + $item.attr('price') + '</strong></p></a><a href="#" class="delete">Delete</a></li>';
            }
    }
}*/

$( document ).on( "pageinit", "#sample-page", function() {
    // Swipe to remove list item
    $( document ).on( "swipeleft swiperight", "#list li.ui-li", function( event ) {
        var listitem = $( this ),
            // These are the classnames used for the CSS transition
            dir = event.type === "swipeleft" ? "left" : "right",
            // Check if the browser supports the transform (3D) CSS transition
            transition = $.support.cssTransform3d ? dir : false;
            confirmAndDelete( listitem, transition );
    });
    // If it's not a touch device...
    if ( ! $.mobile.support.touch ) {
        // Remove the class that is used to hide the delete button on touch devices
        $( "#list" ).removeClass( "touch" );
        // Click delete split-button to remove list item
        $( ".delete" ).on( "click", function() {
            var listitem = $( this ).parent( "li.ui-li" );
            confirmAndDelete( listitem );
        });
    }
    function confirmAndDelete( listitem, transition ) {
        // Highlight the list item that will be removed
        listitem.addClass( "ui-btn-down-d" );
        // Inject topic in confirmation popup after removing any previous injected topics
        $( "#confirm .topic" ).remove();
        listitem.find( ".topic" ).clone().insertAfter( "#question" );
        // Show the confirmation popup
        $( "#confirm" ).popup( "open" );
        // Proceed when the user confirms
        $( "#confirm #yes" ).on( "click", function() {
            // Remove with a transition
            if ( transition ) {
                listitem
                    // Remove the highlight
                    .removeClass( "ui-btn-down-d" )
                    // Add the class for the transition direction
                    .addClass( transition )
                    // When the transition is done...
                    .on( "webkitTransitionEnd transitionend otransitionend", function() {
                        // ...the list item will be removed
                        listitem.remove();
                        // ...the list will be refreshed and the temporary class for border styling removed
                        $( "#list" ).listview( "refresh" ).find( ".ui-li.border" ).removeClass( "border" );
                    })
                    // During the transition the previous list item should get bottom border
                    .prev( "li.ui-li" ).addClass( "border" );
            }
            // If it's not a touch device or the CSS transition isn't supported just remove the list item and refresh the list
            else {
                listitem.remove();
                $( "#list" ).listview( "refresh" );
            }
        });
        // Remove active state and unbind when the cancel button is clicked
        $( "#confirm #cancel" ).on( "click", function() {
            listitem.removeClass( "ui-btn-down-d" );
            $( "#confirm #yes" ).off();
        });
    };
});

itemCount = 0;

var app = {
    // Application Constructor
    initialize: function() {
        this.bindEvents();
    },
    // Bind Event Listeners
    //
    // Bind any events that are required on startup. Common events are:
    // `load`, `deviceready`, `offline`, and `online`.
    bindEvents: function() {
        //document.addEventListener('deviceready', this.onDeviceReady, false);
        document.getElementById('scan').addEventListener('click', this.scan, false);
        //document.getElementById('encode').addEventListener('click', this.encode, false);
    },

    // deviceready Event Handler
    //
    // The scope of `this` is the event. In order to call the `receivedEvent`
    // function, we must explicity call `app.receivedEvent(...);`
    onDeviceReady: function() {
        app.receivedEvent('deviceready');
    },

    // Update DOM on a Received Event
    receivedEvent: function(id) {
        var parentElement = document.getElementById(id);
        var listeningElement = parentElement.querySelector('.listening');
        var receivedElement = parentElement.querySelector('.received');

        listeningElement.setAttribute('style', 'display:none;');
        receivedElement.setAttribute('style', 'display:block;');

        console.log('Received Event: ' + id);
    },

    scan: function() {
        console.log('scanning');
        
        var scanner = cordova.require("cordova/plugin/BarcodeScanner");

        scanner.scan( function (result) { 

            var html1 = '<li> <a href="#demo-mail"><h3>Coke 251mL</h3><img src="img/Coke.jpg" class="ui-li-thumb" /><p class="ui-li-aside"><strong>$1.55</strong></p></a><a href="#" class="delete">Delete</a></li>';
            var html2 = '<li> <a href="#demo-mail"><h3>Yoplait Cherry</h3><img src="img/yogurt.jpg" class="ui-li-thumb" /><p class="ui-li-aside"><strong>$0.98</strong></p></a><a href="#" class="delete">Delete</a></li>';
            var html3 = '<li> <a href="#demo-mail"><h3>Sprite 251mL</h3><img src="img/album-bb.jpg" class="ui-li-thumb" /><p class="ui-li-aside"><strong>$2.07</strong></p></a><a href="#" class="delete">Delete</a></li>';
            
            switch (itemCount) {
            case 0:
                $( "#list" ).append(html1);
                break;
            case 1:
                $( "#list" ).append(html2);
                break;
            case 2:
                $( "#list" ).append(html3);
                break;
            }

            $( "#info" ).hide();

            itemCount++;
            $( "#list" ).listview( "refresh" ).find( ".ui-li.border" ).removeClass( "border" );

            /*
            alert("We got a barcode\n" + 
            "Result: " + result.text + "\n" + 
            "Format: " + result.format + "\n" + 
            "Cancelled: " + result.cancelled);  
            */

           console.log("Scanner result: \n" +
                "text: " + result.text + "\n" +
                "format: " + result.format + "\n" +
                "cancelled: " + result.cancelled + "\n");
            document.getElementById("info").innerHTML = result.text;
            console.log(result);
            /*
            if (args.format == "QR_CODE") {
                window.plugins.childBrowser.showWebPage(args.text, { showLocationBar: false });
            }
            */

        }, function (error) { 
            console.log("Scanning failed: ", error); 
        } );
    },

    encode: function() {
        var scanner = cordova.require("cordova/plugin/BarcodeScanner");

        scanner.encode(scanner.Encode.TEXT_TYPE, "http://www.nhl.com", function(success) {
            alert("encode success: " + success);
          }, function(fail) {
            alert("encoding failed: " + fail);
          }
        );

    }
};

app.initialize();
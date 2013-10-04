<div class="row">
%if cameras is not None:
    <div id="carousel-example-generic" class="carousel slide col-md-6">
        <!-- Indicators -->
        <ol class="carousel-indicators">
    %for num, camera in enumerate(cameras):
            <li data-target="#carousel-example-generic" data-slide-to="{{num}}"></li>
    %end
        </ol>
        <!-- Wrapper for slides -->
        <div class="carousel-inner">
    %for num, camera in enumerate(cameras):
            <div class="item active">
                <img src="{{camera.get('url', '')}}">
                <div class="carousel-caption">
                 {{camera.get('name', '')}}
                </div>
            </div>
    %end
        </div>
        <!-- Controls -->
        <!--<a class="left carousel-control" href="#carousel-example-generic" data-slide="prev">
            <span class="icon-prev"></span>
        </a>
        <a class="right carousel-control" href="#carousel-example-generic" data-slide="next">
            <span class="icon-next"></span>
        </a>-->
    </div>
%end
%if switches is not None:
    <div class="col-md-3">
        <h4 class="text-muted">Switches</h2>
        <div class="switches">
            <ul class="list-group">
        %for num, switch in enumerate(switches):
                <li class="list-group-item">
                    <div class="btn-group pull-right">
                        <a href="/switch/{{num}}/on" class="btn {{switch.get('state', 0) and "btn-primary" or ""}}">On</a>
                        <a href="/switch/{{num}}/off" class="btn {{ (not switch.get('state', 0)) and "btn-primary" or "" }}">Off</a>
                    </div>
                    <h5>{{ switch["name"] }}</h5>
                </li>
        %end
            </ul>
        </div>
    </div>
%end
%for pg_info in plugin_infos:
    <div class="col-md-3">
        <h4 class="text-muted">{{pg_info["title"]}}</h2>
        <ul class="list-group">
        %for num, item in enumerate(pg_info["items"]):
            <li class="list-group-item">
                <p class="btn-group pull-right">
                    {{ item["value"] }}
                </p>
                {{ item["name"] }}
            </li>
        %end
        </ul>
    </div>
%end
</div>
%rebase base title=('Manage')

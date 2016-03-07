% rebase('base.tpl')
<script type="text/javascript">
    $(document).ready(function() {
        info = new Highcharts.Chart({
            chart: {
                renderTo: 'load',
                margin: [0, 0, 0, 0],
                backgroundColor: null,
                plotBackgroundColor: 'none'
            },
            credits: {
                enabled: false
            },
            title: {
                text: null
            },
            tooltip: {
                formatter: function() {
                    return this.point.name +': '+ this.y +' %';
                }
            },
            series: [
                {
                borderWidth: 2,
                borderColor: '#F1F3EB',
                shadow: false,
                type: 'pie',
                name: 'Data Transfer',
                innerSize: '65%',
                data: [
                    { name: 'Incoming', y: {{data['pcnt_in']}}, color: '#b2c831' },
                    { name: 'Outgoing', y: {{data['pcnt_out']}}, color: '#fa1d2d' }
                ],
                dataLabels: {
                    enabled: false,
                    color: '#000000',
                    connectorColor: '#000000'
                }
            }]
        });
    });
</script>
<div class="container">
    <!-- FIRST ROW OF BLOCKS -->
    <div class="row">
        % include('general.tpl', data=data)
        % include('connections.tpl', data=data)
        % include('bandwidth.tpl', data=data)
    </div><!-- /row -->
    <!-- SECOND ROW OF BLOCKS -->
    <div class="row">
        % include('bandwidth_summary.tpl', data=data)
        % include('network.tpl', data=data)
        % include('donate.tpl', data=data)
    </div><!-- /row -->
</div> <!-- /container -->

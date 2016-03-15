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
    % for row in page_info['tiles']:
        <!-- Start of row -->
        <div class="row">
            % for tile_name in row:
                % include(tiles[tile_name]['template'], data=data)
            % end
        </div><!-- /row -->
    % end
</div> <!-- /container -->

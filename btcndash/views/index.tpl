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

      <!-- NODE INFORMATION -->
        <div class="col-sm-4 col-lg-4">
      		<div class="dash-unit">
	      		<dtitle>Bitcoin Node Information</dtitle>
	      		<hr>
	      		<div class="info-user">
					<span aria-hidden="true" class="li_display fs2"></span>
				</div>
				<br/>
				<h1>Bitcoin Full Node</h1>
				<h1>{{data['ip']}}</h1>
				<h3><a href='{{data['map_url']}}'>{{data['loc']}}</a></h3>
				<div class="cont">
				   <p>Stats Last Updated:<br/>{{data['update']}}</p>
				</div>
				</div>
        </div>

        <!-- CONNECTIONS -->
        <div class="col-sm-4 col-lg-4">
      		<div class="half-unit">
	      		<dtitle>Connections</dtitle>
	      		<hr>
		      		<div class="cont">
			      		<h2>{{data['cons']}}</h2>
			      		<h3><a href="/peers">Connected Peers</a></h3>
		      		</div>
			</div>
            <!-- TRANSACTIONS -->
			<div class="half-unit">
	      		<dtitle>Transactions</dtitle>
	      		<hr>
	      		<div class="cont">
					<h2>{{data['tx_count']}}</h2>
			      		<h3><a href="/tx">Recent Transactions</a></h3>
				</div>
			</div>
        </div>
        
        <!-- BANDWIDTH CHART -->
        <div class="col-sm-4 col-lg-4">
      		<div class="dash-unit">
		  		<dtitle>Bandwidth Chart</dtitle>
		  		<hr>
	        	<div id="load"></div>
	        	<h3>{{data['pcnt_in']}}% Incoming Data</h3>
	        	<h3>{{data['pcnt_out']}}% Outgoing Data</h3>
			</div>
        </div>
        
      </div><!-- /row -->
      
	  <!-- BANDWIDTH SUMMARY -->     
      <div class="row">
      
      <div class="col-sm-4 col-lg-4">
      		<div class="dash-unit">
	      		<dtitle>Bandwidth Summary</dtitle>
	      		<hr>
	      		<div class="cont">
					<h2>{{data['sent']}} MB</h2>
					<h3>Sent</h3>
					<h2>{{data['recv']}} MB</h2>
					<h3>Received</h3>
					<h2>{{data['total']}} GB</h2>
					<h3>Total</h3>
				</div>  
			</div>
        </div>
        
	  <!-- NETWORK STATS -->     
        <div class="col-sm-4 col-lg-4">
      		<div class="dash-unit">
      		<dtitle>Network Stats</dtitle>
      		<hr>
			    <div class="cont">
			        <h2>{{data['block_height']}}</a></h2>
					<h3><a href="{{data['block_url']}}">Block Height</a></h3>
			        <h2>{{data['hashrate']}} Th/s</h2>
					<h3><a href='{{data['hash_diff_url']}}'>Hash Rate</a></h3>
					<h2>{{data['diff']}}</a></h2>
					<h3><a href='{{data['hash_diff_url']}}'>Difficulty</a></h3>
			    </div>
			</div>
        </div>

	  <!-- DONATE ADDRESS -->     
        <div class="col-sm-4 col-lg-4">
      		<div class="dash-unit">
	      		<dtitle>Donate Address</dtitle>
	      		<hr>
				<div class="cont">
				     <p><a href='https://blockchain.info/address/{{data['donate']}}'><img src='{{data['qr_url']}}' alt='QRCode' /></a></p>
				</div>   
			</div>
        </div>
        
      </div><!-- /row -->    
      
	</div> <!-- /container -->

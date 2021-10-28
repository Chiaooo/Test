var ec_left2 = echarts.init(document.getElementById("l2"),"vintage");

var option_left2 = {
      	title: {
      		text: '全国新增趋势',
			textStyle: {
				color:"#3398DB"
			},
			left: 'left'
      	},
		
      	legend: {
      		data: ['新增确诊', '新增疑似'],
			left: 'right'
      	},

      	grid: {
      		top: 50,
      		left: '4%',
      		right: '6%',
      		bottom: '4%',
      		containLabel: true
      	},

      	tooltip: {
      		trigger: 'axis',
			axisPointer: {
				type: 'line',
				lineStyle: {
					color: '#7171C6'
				}
			}
      	},

      	xAxis: {
      		type: 'category',
      		data: []
      	},
		axisLabel: {
      	color:"#3398DB"
		},

      	yAxis: {
      		type: 'value',
      		axisLine: {
				show: true
      		},
			axisLabel: {
				show: true,
				color: '#3398DB',
				fontSize: 15,
				formatter: function(value) {
					if (value >= 1000) {
						value = value / 1000 + 'k';
					}
					return value;
				}
			},
			splitLine: {
				show: true,
				lineStyle: {
					color: '#172738',
					width: 1,
					type: 'solid'
				}
			}
      	},

      	series: [{
      			name: '新增确诊',
      			data: [],
      			type: 'line',
      			smooth: true
      		},

      		{
      			name: '新增疑似',
      			data: [],
      			type: 'line',
      			smooth: true
      		}
      	]
      };
	  
ec_left2.setOption(option_left2);

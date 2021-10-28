var ec_left1 = echarts.init(document.getElementById("l1"),"vintage");

var option_left1 = {

      	title: {
      		text: '全国累计趋势',
			textStyle: {
      			color:"#3398DB"
			},
			left: 'left'
      	},
		
      	legend: {
      		data: ['累计确诊', '现有疑似', '累计治愈','累计死亡'],
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
      			name: '累计确诊',
      			data: [],
      			type: 'line',
      			smooth: true
      		},

      		{
      			name: '现有疑似',
      			data: [],
      			type: 'line',
      			smooth: true
      		},

      		{
      			name: '累计治愈',
      			data: [],
      			type: 'line',
      			smooth: true
      		},
			
			{
				name: '累计死亡',
				data: [],
				type: 'line',
				smooth: true
			}
      	]
      };
	  
ec_left1.setOption(option_left1);

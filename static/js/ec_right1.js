var ec_right1 = echarts.init(document.getElementById("r1"),"vintage");

option_right1 = {
	title: {
		text: '非湖北地区城市确诊TOP5',
		textStyle: {
			color: '#3398DB'
		},
		left: 'left'
	},

	color: ['#3398DB'],
	tooltip: {
		trigger: 'axis',
		axisPointer: {
			type: 'shadow'
		}
	},

	xAxis: {
		type: 'category',
		data: [],
		axisLabel: {
			color:"#3398DB",
			fontSize:15
		},
	},

	yAxis: {
		type: 'value',
		//坐标轴刻度设置
		axisLabel: {
      		color:"#3398DB",
			fontSize:15
		},
	},

	series: [{
		type: 'bar',
		data: [],
		barMaxWidth: "50%"
	}]
};
ec_right1.setOption(option_right1)

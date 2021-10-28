var ec_right2 = echarts.init(document.getElementById("r2"), "vintage");

var option_right2 = {
	title: {
		text: "今日热搜",
		textStyle: {
			color: '#3398DB'
		},
		left: 'left'
	},
	tooltip: {
		show: false
	},
	series: [{
		type: 'wordCloud',
		gridSize: 1,
		sizeRange: [12, 55],
		rotationRange: [-45, 0, 45, 90],
		textStyle: {
			normal: {
				color: function() {
					return 'rgb(' +
						Math.round(Math.random() * 255) +
						',' + Math.round(Math.random() * 255) +
						',' + Math.round(Math.random() * 255) + ')'
				}
			}
		},
		right: null,
		bottom: null
	}]
};
ec_right2.setOption(option_right2);

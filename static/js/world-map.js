let worldMap = echarts.init(document.getElementById('world'))

window.addEventListener('resize', function () {
worldMap.resize()
})
// 绘制图表
worldMap_option = {
// 图表主标题
    title: {
      top: 20,
      left: 'center',
      textStyle: { // 文本样式
        fontSize: 28,
        fontWeight: 600,
        color: '#4969c9'
      }
    },
    backgroundColor:'#fef8ef',
    tooltip: {
      trigger: 'item',
    },
    // 视觉映射组件
    visualMap: {
      type: 'piecewise',
      show: true,
      // 文本样式
      x:'10%',
      y:'65%',
      textStyle: {
        fontSize: 18,
        color: 'black'
      },
      realtime: false,
      calculable: true,
      splitList:[
        {start:1,end:4999},
        {start:5000,end:49999},
        {start:50000,end:199999},
        {start:200000,end:500000},
        {start:500000,end:999999},
          {start:1000000},
      ],
      inRange: {
          color: ['#f8c291', '#f6b93b','#e58e26','#e55039', '#eb2f06', '#9B1A1A']
      }
    },
    series: [
             {
                type: 'map',
                name: '累计确诊',
                mapType: 'world',
                roam: false,
                zoom : 1.2,
                itemStyle: {
                  areaColor: '#fad390',
                  borderWidth: 0.5,
                  borderColor: '#333',
                  borderType: 'solid'
                },
                emphasis: {
                  label: {
                        show: true,
                        fontSize:16,
                        fontWeight:600,
                        color: '#6868ff'
                  },

                  itemStyle: {
                    areaColor: '#FD6666'
                  }
                },
                nameMap: name,
            },
        ]
};

worldMap.setOption(worldMap_option)

<template>
  <div>
    <div class="question-box">
      <div class="word">
        <h1 class="questionNumber" v-model="index">
          Q{{ index + 1 }} {{ questionData.type }}
        </h1>
        <h2 class="questionName" v-model="questionData">
          {{ questionData.title }}
        </h2>
      </div>
      <el-carousel :autoplay="false" indicator-position="outside">
        <el-carousel-item style="background-color: #fff" :key="'chart'">
          <div id="chart">
            <apexchart
              height="300px"
              type="bar"
              :options="chartOptions"
              :series="series"
            ></apexchart>
          </div>
        </el-carousel-item>
        <el-carousel-item
          style="background-color: #fff"
          v-for="(el, i) in tableDataList"
          :key="i"
        >
          <el-table :data="el.data" style="width: 100%">
            <el-table-column prop="field" label="Field" width="200px">
            </el-table-column>

            <el-table-column
              v-for="(el2, idx) in parTableConfig"
              :prop="String(idx + 1)"
              :label="String(idx + 1)"
              :key="idx"
              :formatter="(r, c, cellValue) => cellValue || '0'"
            >
            </el-table-column>
            <el-table-column fixed="right" label="Total" width="100">
              <template slot-scope="scope">
                {{
                  parTableConfig.reduce(
                    (pv, cv, id) => (scope.row[String(id + 1)] || 0) + pv,
                    0
                  )
                }}
              </template>
            </el-table-column>
          </el-table>
        </el-carousel-item>
      </el-carousel>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: 'MultipleChoiceResult',
  props: {
    question: Object,
    index: Number,
  },
  data() {
    return {
      tableDataList: [{}],
      parTableConfig: [],
      questionData: '',
      number: 0,
      series: [],
      chartOptions: {
        chart: {
          type: 'bar',
          height: 350,
        },
        plotOptions: {
          bar: {
            horizontal: true,
            columnWidth: '55%',
            endingShape: 'rounded',
          },
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          show: true,
          width: 2,
          colors: ['transparent'],
        },
        xaxis: {},
        // yaxis: {
        //   title: {
        //     text: '$ (thousands)'
        //   }
        // },
        fill: {
          opacity: 1,
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return val
            },
          },
        },
      },
    }
  },
  methods: {},
  created() {
    this.number = this.index
    this.questionData = this.question
    const parTableConfig = JSON.parse(this.question.tableConfig)
    this.parTableConfig = parTableConfig
    const parColumnConfig = JSON.parse(this.question.columnConfig)
    const parAnswers = this.question.answers.map((e) =>
      JSON.parse(e.replace(/\'/g, '"'))
    )
    const categories = parTableConfig.map((el) => el.name)
    const series = parColumnConfig.map((el) => {
      return {
        name: el.label,
        data: categories.map((el2) => {
          let num = 0

          parAnswers.map((it) => {
            it.forEach((itc) => {
              if (itc.label === el.label) {
                itc.children.forEach((itcc) => {
                  if (itcc.name === el2) {
                    num++
                  }
                })
              }
            })
          })
          return num
        }),
      }
    })
    this.series = series
    this.chartOptions.xaxis.categories = categories
    this.tableDataList = parColumnConfig.map((el, idx) => {
      //el {label: 'Label1', value: 'e', children: Array(0)}
      return {
        label: el.label,
        value: el.value,
        data: parTableConfig.map((el2) => {
          //el2 {name: 'Choice1'}
          const ret = {
            field: el2.name,
          }
          parAnswers.forEach((el4, idx4) => {
            el4[idx].children.forEach((el5, idx5) => {
              //el5 {name: 'Choice1', type: 'root'}
              if (el5.name === el2.name) {
                if (ret[idx5 + 1]) {
                  ret[idx5 + 1]++
                } else {
                  ret[idx5 + 1] = 1
                }
              }
            })
          })
          return ret
        }),
      }
    })
    debugger

    // function string2int(list) {
    //   let res = [];
    //   for (let i = 0; i < list.length; i++) {
    //     res[i] = Number(list[i]);
    //   }
    //   return res;
    // }

    // this.chartOptions.xaxis.categories = this.question.x;
    // this.series[0].data = string2int(this.question.y);
  },
  // data() {
  //   return {
  //     questions: {
  //       "id": 3,
  //       "block": 2,
  //       "name": "How esay does it use?",
  //       "type": "Multiple choice",
  //       "description": "",
  //       "order": 2,
  //       "count": 60,
  //       "choices": [
  //         {
  //           "id": 4,
  //           "question": 2,
  //           "order": 1,
  //           "title": "A",
  //           "number": 20,
  //           "percentage": 0.2
  //         },
  //         {
  //           "id": 5,
  //           "question": 2,
  //           "order": 2,
  //           "title": "B",
  //           "number": 80,
  //           "percentage": 0.8
  //         }
  //       ]
  //     },
  //     series: [{
  //       data: [44.4, 33.3, 11.1, 11.1]
  //     }],
  //     chartOptions: {
  //       chart: {
  //         type: 'bar',
  //         height: 350
  //       },
  //       plotOptions: {
  //         bar: {
  //           borderRadius: 4,
  //           horizontal: true,
  //           dataLabels: {
  //             position: 'top',
  //           }
  //         }
  //       },
  //       dataLabels: {
  //         enabled: true,
  //         offsetX: -6,
  //         style: {
  //           fontSize: '12px',
  //           colors: ['#fff']
  //         }
  //       },
  //       xaxis: {
  //         categories: ['Super easy', 'Easy enough', 'A tad difficult', 'Way to difficult'],
  //       }
  //     }
  //   }
  // }
}
</script>
<style>
.questionAVG {
  color: red;
  font-size: 20px;
  margin-left: 370px;
}

.question-box {
  width: 550px;
  border: 2px solid #eff2f5;
  border-radius: 4px;
  margin: 20px;
  padding: 8px;
}
</style>

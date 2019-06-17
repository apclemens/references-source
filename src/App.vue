<template>
  <div id="app">
      <div
          id="hover_info"
          v-bind:style="{left: clientX, top: clientY, display: hovering ? 'block' : 'none'}"
      >
          In <div id="hover_year">{{hover_year}}</div> there {{werewas}} a total of
          <div id="hover_number">{{hover_number}}</div> reference{{references}} to
          movies from <div id="hover_ref">{{hover_ref}}</div>
      </div>
      <div id="graph_title" v-bind:style="{width: ''+graph_width+'px'}">
          <h2>
              Frequency of movie references from one year to another
          </h2>
      </div>
      <svg id="chart" v-bind:width="graph_width" v-bind:height="graph_width">
          <rect width="100%" height="100%" fill="#dcdaf9"/>
          <line
                v-bind:x1="0"
                v-bind:y1="graph_width-30"
                v-bind:x2="graph_width"
                v-bind:y2="graph_width-30"
                style="stroke: black"
          />
          <line
                v-bind:x1="30"
                v-bind:y1="0"
                v-bind:x2="30"
                v-bind:y2="graph_width"
                style="stroke: black"
          />
          <text
                v-for="n in 11"
                v-bind:x="a*1900+10*a*n+b"
                v-bind:y="graph_width-35"
                v-bind:key="'x_'+n"
                fill="black"
                font-family="Arial"
          >
                {{1900+10*n}}
          </text>
          <text
                v-for="n in 11"
                v-bind:x="35"
                v-bind:y="graph_width-a*1900-10*a*n-b"
                v-bind:key="'y_'+n"
                fill="black"
                font-family="Arial"
          >
                {{1900+10*n}}
          </text>
          <text
                v-bind:x="-graph_width/2"
                v-bind:y="15"
                style="transform: rotate(-90deg)"
                font-family="Arial"
          >
                Reference year
          </text>
          <text
                v-bind:x="graph_width/2"
                v-bind:y="graph_width-10"
                font-family="Arial"
          >
                Movie year
          </text>
          <rect
                v-for="data in combinations"
                class="data_cell"
                v-bind:x="a*data[0]+b"
                v-bind:y="graph_width-a*data[1]-b"
                v-bind:width="a"
                v-bind:height="a"
                v-bind:style="'fill:rgb('+(255-255*data[2]/highest_value)+','+(255-255*data[2]/highest_value)+','+(255-255*data[2]/highest_value)+')'"
                v-bind:class="{selected: data[0]==selected_year&&data[1]==selected_ref}"
                @mouseover="mouseOverCell"
                @mouseout="mouseOutCell"
                v-on:click="clickCell"
                v-bind:id="data[0]+'-'+data[1]+'-'+data[2]"
                v-bind:key="data[0]+'-'+data[1]+'-'+data[2]"
          />
          <line
                v-for="n in 11"
                v-bind:x1="0"
                v-bind:y1="graph_width-a*1900-10*a*n-b"
                v-bind:x2="graph_width"
                v-bind:y2="graph_width-a*1900-10*a*n-b"
                style="stroke: grey"
          />
          <line
                v-for="n in 11"
                v-bind:x1="a*1900+10*a*n+b"
                v-bind:y1="0"
                v-bind:x2="a*1900+10*a*n+b"
                v-bind:y2="graph_width"
                style="stroke: grey"
          />
      </svg>
      <div v-if="selected" id="reference_info" v-bind:style="'width: '+graph_width+'px'">
          <h2>
              References to {{selected_ref}} from {{selected_year}}
          </h2>
          <ul>
              <li
                   v-for="movie in Object.keys(data[selected_year][selected_ref][1])"
                   v-bind:key="movie"
              >
                {{movie}}
                <ul>
                      <li
                         v-for="reference in data[selected_year][selected_ref][1][movie]"
                         v-bind:key="reference"
                      >
                        {{reference}}
                      </li>
                </ul>
              </li>
          </ul>
      </div>
  </div>
</template>

<script>
import data from './json/data.json'

export default {
  name: 'app',
  data() {
      const GRAPH_WIDTH = 600;
      var lowest_year = 2000;
      var highest_year = 0;
      var highest_value = 0;
      var combinations = [];
      Object.keys(data).forEach(function(year){
          Object.keys(data[year]).forEach(function(ref){
              if(Number(ref) < lowest_year) lowest_year = Number(ref);
              if(Number(ref) > highest_year) highest_year = Number(ref);
              if(data[year][ref][0] > highest_value) highest_value = data[year][ref][0];
              combinations.push([Number(year), Number(ref), data[year][ref][0]]);
          })
      })
      var a = GRAPH_WIDTH / (highest_year + 1 - lowest_year)
      var b = -a * lowest_year
      return {
          hovering: false,
          combinations: combinations,
          lowest_year: lowest_year,
          highest_year: highest_year,
          highest_value: highest_value,
          graph_width: GRAPH_WIDTH,
          a: a,
          b: b,
          clientX: '',
          clientY: '',
          hover_year: '',
          hover_ref: '',
          hover_number: '',
          werewas: 'were',
          references: 's',
          data: data,
          selected: false,
          selected_year: '',
          selected_ref: '',
      }
  },
  methods: {
      mouseOverCell: function(e) {
          this.hovering = true
          this.clientX = ''+e.layerX+'px'
          this.clientY = ''+(e.layerY-20)+'px'
          this.hover_year = e.target.id.split("-")[0]
          this.hover_ref = e.target.id.split("-")[1]
          this.hover_number = e.target.id.split("-")[2]
          this.werewas = this.hover_number == 1 ? 'was' : 'were'
          this.references = this.hover_number == 1 ? '' : 's'
      },
      mouseOutCell: function() {
          this.hovering = false
      },
      clickCell: function(e) {
          this.selected = true
          this.selected_year = e.target.id.split("-")[0]
          this.selected_ref = e.target.id.split("-")[1]
      },
  }
}
</script>

<style>
#hover_info {
    position: absolute;
    pointer-events: none;
    width: 165px;
    text-align: center;
    background-color: rgba(255, 255, 255, .5);
    transform: translate(-50%, 30px);
    padding: 10px;
    font-family: Arial;
}
#hover_year, #hover_ref {
    font-size: 150%;
}
#hover_number {
    font-size: 250%;
}
.data_cell:hover {
    fill: red !important;
}
#reference_info {
    font-family: Arial;
}
#graph_title {
    background-color: #dcdaf9;
    text-align: center;
    font-family: Arial;
    padding: 10px 0;
}
#graph_title h2 {
    margin: 0;
}
</style>

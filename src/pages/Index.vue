<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <q-page>
    <div class="row">
      <div class="fa-align-center col-lg-grow q-pa-lg">
        <q-toolbar>
          <q-btn @click="addTable" round dense icon="add">
            <q-tooltip :delay="300" content-style="font-size: 12px">Добавить таблицу</q-tooltip>
          </q-btn>
          <q-btn round dense icon="save" @click="exportExcel">
            <q-tooltip :delay="300" content-style="font-size: 12px">Сохранить в Excel</q-tooltip>
          </q-btn>
        </q-toolbar>
        <report-table v-for="tab in refTables" :key="tab.id" :table="tab"
                      @ontabledelete="onTableDelete"
                      @ontablecopy="onTableCopy"/>
      </div>
    </div>
  </q-page>
</template>

<script>
import ReportTable from '../components/ReportTable.vue'

export default {
  data () {
    return {
      refTables: [
        {
          id: 1,
          rows: null,
          header: 'A380',
          columns: [
            {
              name: 1,
              label: 'F1, ГГц',
              field: row => row[0],
              condition: 'Uп = 4,5В\nsecond condition',
              norms: 'не более 1,9',
              index: 0,
              mid: 1.5,
              spread: 0.5,
              step: 0.1,
              align: 'center'
            },
            {
              name: 2,
              label: 'f2, ГГЦ',
              field: row => row[1],
              condition: 'Uп = 4.5 В',
              norms: 'не менее 12,3',
              index: 1,
              mid: 2.5,
              spread: 0.1,
              step: 0.1,
              align: 'center'
            }
          ],
          data: [
            [1, 2, 3],
            [1, 2, 3]
          ]
        },
        {
          id: 2,
          rows: null,
          header: 'A381',
          columns: [
            {
              name: 1,
              label: 't1, нс',
              field: row => row[0],
              condition: 'Uп = 4.5 В',
              norms: 'не более 25',
              index: 0,
              mid: 1.5,
              spread: 0.5,
              step: 0.1,
              align: 'center'
            },
            {
              name: 2,
              label: 'I, мА',
              field: row => row[1],
              condition: 'Uп = 5.5 В',
              norms: 'не более 100',
              index: 1,
              mid: 1.5,
              spread: 0.5,
              step: 0.1,
              align: 'center'
            }
          ],
          data: [
            [3, 4, 5],
            [3, 4, 5]
          ]
        }
      ]
    }
  },
  methods: {
    onTableDelete (tableId) {
      let index = this.refTables.findIndex(tab => tab.id === tableId)
      this.refTables.splice(index, 1)
    },
    onTableCopy (tableId) {
      let tableToCopy = this.refTables.find(tab => tab.id === tableId)

      let columns = []
      tableToCopy.columns.forEach(col => {
        let newCol = {
          label: col.label,
          condition: col.condition,
          norms: col.norms,
          mid: col.mid,
          spread: col.spread,
          step: col.step,
          align: col.align,
          index: col.index,
          field: col.field,
          name: col.name
        }
        columns.push(newCol)
      })

      let newTable = JSON.parse(JSON.stringify({
        id: tableToCopy.id,
        rows: tableToCopy.rows,
        header: tableToCopy.header,
        columns: columns,
        data: []
      }))

      let [lastTable] = this.refTables.slice(-1)
      if (!lastTable) {
        lastTable = {
          id: 1
        }
      }

      newTable.id = lastTable.id + 1
      this.refTables.push(newTable)
    },
    generateValue (mid, spread, step) {
      let randint = (min, max) => {
        return Math.floor(Math.random() * (max - min + 1) + min)
      }
      if (!mid || !spread || !step) { return 0 }
      const min = mid - spread
      const max = mid + spread
      let res = randint(0, (max - min) / step) * step + min
      return res.toFixed(1)
    },
    generateTables () {
      this.tables.forEach(t => {
        this.generateTableValues(t.id)
      })
    },
    generateTableValues (tableId) {
      let table = this.tables[tableId]
      let rows = table.rows < 0 ? 0 : table.rows
      let result = []
      for (let i = 0; i < rows; i++) {
        let newRow = {}
        this.columns.forEach(col => {
          if (typeof col.colIndex === 'undefined') {
            return
          }
          newRow[col.colIndex] = this.generateValue(col.mid, col.spread, col.step)
        })
        newRow['name'] = i + 1
        result.push(newRow)
      }
      table.data = result
      table.rows = rows
    },
    addTable () {
      let newId = this.refTables.length ? this.refTables[this.refTables.length - 1].id + 1 : 0
      this.refTables.push({
        id: newId,
        rows: null,
        header: '',
        columns: [],
        data: []
      })
    },
    copyTable () {
      console.log('copy table')
    },
    async exportExcel () {
      let cols = []
      this.columns.forEach(col => {
        let colData = {
          label: col.label,
          condition: col.condition,
          norms: col.norms,
          index: col.colIndex
        }
        cols.push(colData)
      })

      let tables = []
      this.tables.forEach(table => {
        let tableData = {
          header: table.header,
          data: table.data
        }
        tables.push(tableData)
      })

      const rawResponse = await fetch('http://localhost:5000/api', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
          cols: cols,
          tables: tables
        })
      })

      let d = await rawResponse.body.getReader().read()
      let dt = d.value

      const url = window.URL.createObjectURL(new Blob([dt]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'out.xlsx')
      document.body.appendChild(link)
      link.click()
    }
  },
  mounted () {
  },
  components: {
    ReportTable
  }
}
</script>

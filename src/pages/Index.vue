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
        <report-table v-for="tab in tables" :key="tab.id" :table="tab"
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
      tables: [
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
          data: []
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
          data: []
        }
      ]
    }
  },
  methods: {
    onTableDelete (tableId) {
      let index = this.tables.findIndex(tab => tab.id === tableId)
      this.tables.splice(index, 1)
    },
    onTableCopy (tableId) {
      let tableToCopy = this.tables.find(tab => tab.id === tableId)

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

      let [lastTable] = this.tables.slice(-1)
      if (!lastTable) {
        lastTable = {
          id: 1
        }
      }

      newTable.id = lastTable.id + 1
      this.tables.push(newTable)
    },
    addTable () {
      let newId = this.tables.length ? this.tables[this.tables.length - 1].id + 1 : 0
      this.tables.push({
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

<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <q-page>
    <div class="row">
      <div class="col-lg-3 q-pa-sm">
        <q-toolbar>
          <q-btn round icon="add"/>
        </q-toolbar>
        <q-scroll-area style="height: 800px;">
          <q-list bordered>
            <q-item v-for="col in columns.slice(1)" v-bind:key="col.name" clickable>
              <q-item-section top>
                <q-item-label lines="1">
                  <span class="text-grey-10">{{ col.label }}</span>
                </q-item-label>
                <q-item-label caption lines="1">
                  {{ col.condition }}
                </q-item-label>
                <q-item-label lines="1" class="q-mt-xs">
                  {{ col.norms }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                  <div class="col-sm">среднее={{ col.mid }}</div>
                  <div class="col-sm">разброс={{ col.spread }}</div>
                  <div class="col-sm">шаг={{ col.step }}</div>
              </q-item-section>
              <q-item-section side>
                <div class="text-grey-8 q-gutter-xs">
                  <q-btn class="gt-xs" size="12px" flat dense round icon="edit" @click="onEditColumn(col)"/>
                  <q-btn class="gt-xs" size="12px" flat dense round icon="delete" @click="onDeleteColumn(col)"/>
                </div>
              </q-item-section>
            </q-item>

            <q-separator/>

          </q-list>
        </q-scroll-area>
      </div>
      <div class="col-lg-9 q-pa-sm">
        <q-table
          title="Отчёт"
          dense
          :data="data"
          :columns="columns"
          row-key="name"
        >
          <template v-slot:header-cell="props">
            <q-th :props="props">
              {{ props.col.label }}<br/>
              {{ props.col.condition }}<br/>
              {{ props.col.norms }}
            </q-th>
          </template>
        </q-table>
      </div>
    </div>

    <q-dialog v-model="dlgEditColumn">
      <q-card style="width: 500px" class="q-px-sm">

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.label" label="Параметр:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.condition" label="Условие:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.norms" label="Норма:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.mid" type="number" label="Среднее:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.spread" type="number" label="Разброс:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.step" type="number" label="Шаг:" dense/>
          </q-item-section>
        </q-item>

        <q-item>
          <q-btn primary small color="primary" label="ОК" @click="onDlgAccept"/>
        </q-item>
      </q-card>

    </q-dialog>
  </q-page>
</template>

<script>
export default {
  data () {
    return {
      leftDrawer: true,
      dlgEditColumn: false,
      columnEditObj: {
        name: null,
        label: '',
        align: 'left',
        field: row => {},
        condition: '',
        norms: '',
        mid: 0,
        spread: 0,
        step: 0
      },
      columns: [
        { name: 0, label: '№ миксросхемы', norms: '', condition: '', field: 'name', align: 'left' },
        {
          name: 1,
          label: 'F1, ГГц',
          align: 'left',
          field: row => row[0],
          condition: 'Uп = 4,5В',
          norms: 'не более 1,9',
          mid: 1.5,
          spread: 0.5,
          step: 0.1
        },
        {
          name: 2,
          label: 'f2, ГГЦ',
          field: row => row[1],
          align: 'center',
          condition: 'Uп = 4.5 В',
          norms: 'не менее 12,3',
          mid: 2.5,
          spread: 0.1,
          step: 0.1
        },
        {
          name: 3,
          label: 'D, дБ',
          field: row => row[2],
          condition: 'Uп = 4.5 В',
          norms: 'не менее 51',
          mid: 1.5,
          spread: 0.5,
          step: 0.1
        },
        {
          name: 4,
          label: 'Pвх мин, дБм',
          field: row => row[3],
          condition: 'Uп = 4.5 В',
          norms: 'не более -41',
          mid: 1.5,
          spread: 0.5,
          step: 0.1
        },
        {
          name: 5,
          label: 't1, нс',
          field: row => row[4],
          condition: 'Uп = 4.5 В',
          norms: 'не более 25',
          mid: 1.5,
          spread: 0.5,
          step: 0.1
        },
        {
          name: 6,
          label: 'I, мА',
          field: row => row[5],
          condition: 'Uп = 5.5 В',
          norms: 'не более 100',
          mid: 1.5,
          spread: 0.5,
          step: 0.1
        }
      ],
      data: [
        {
          name: 1,
          0: 1.5,
          1: 12.8,
          2: 56.0,
          3: -44,
          4: 20,
          5: 34
        },
        {
          name: 2,
          0: 1.6,
          1: 12.9,
          2: 57.0,
          3: -47,
          4: 23,
          5: 36
        }
      ]
    }
  },
  methods: {
    onEditColumn (col) {
      this.dlgEditColumn = true
      this.columnEditObj = { ...col }
    },
    onDeleteColumn (col) {
      this.columns.splice(this.columns.indexOf(col), 1)
    },
    onDlgAccept (event) {
      this.dlgEditColumn = false
      let index = this.columns.findIndex(el => this.columnEditObj.name === el.name)
      if (index === -1) {
        this.addColumn()
        return
      }
      this.editColumn(index)
      console.log(this.columns)
    },
    editColumn (index) {
      let found = this.columns[index]
      found.label = this.columnEditObj.label
      found.condition = this.columnEditObj.condition
      found.norms = this.columnEditObj.norms
      found.mid = this.columnEditObj.mid
      found.spread = this.columnEditObj.spread
      found.step = this.columnEditObj.step
    },
    addColumn () {
      alert('add column')
    }
  }
}
</script>

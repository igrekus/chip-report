<template>
  <q-page>
    <div class="row">
      <div class="col-lg-3 q-pa-sm">
        <q-toolbar>
          <q-btn round icon="add"/>
        </q-toolbar>
        <q-scroll-area style="height: 800px;">
          <q-list bordered>
            <q-item v-for="col in columns" v-bind:key="col.name">
              <q-item-section top>
                <q-item-label lines="1">
                  <span class="text-grey-10">{{ col.label }}</span>
                </q-item-label>
                <q-item-label caption lines="1">
                  parameters
                </q-item-label>
                <q-item-label lines="1" class="q-mt-xs">
                  norms
                </q-item-label>
                <div class="row">
                  <q-input v-model="text" class="col-sm" label="mid" dense/>
                  <q-input v-model="text" class="col-sm q-pa-sm" label="spread" dense/>
                  <q-input v-model="text" class="col-sm" label="step" dense/>
                </div>
              </q-item-section>

              <q-item-section side>
                <div class="text-grey-8 q-gutter-xs">
                  <q-btn class="gt-xs" size="12px" flat dense round icon="delete"/>
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
        />
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  data () {
    return {
      leftDrawer: true,
      columns: [
        {
          name: 1,
          label: 'f1, ГГц',
          required: true,
          align: 'left',
          field: row => row.name,
          format: val => `${val}`,
          sortable: true
        },
        { name: 2, label: 'f2, ГГЦ', field: 'calories', sortable: true, align: 'center' },
        { name: 3, label: 'D, дБ', field: 'fat', sortable: true },
        { name: 4, label: 'Pвх мин, дБм', field: 'carbs' },
        { name: 5, label: 't1, нс', field: 'protein' },
        { name: 6, label: 'I, мА', field: 'sodium' }
      ],
      data: [
        {
          name: 'Frozen Yogurt',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          sodium: 87,
          calcium: '14%',
          iron: '1%'
        },
        {
          name: 'Ice cream sandwich',
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3,
          sodium: 129,
          calcium: '8%',
          iron: '1%'
        }
      ]
    }
  }
}
</script>

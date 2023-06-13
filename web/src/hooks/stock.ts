import { ref } from "vue";
import { Stock } from "@/apis/typings";
import { getStockList } from "@/apis/stock";

export const useStockList = (emit: any) => {
  let firstLoaded = false;

  const form = ref({
    page_current: 1,
    page_size: 1000
  });

  const list = ref<Stock[]>([]);
  const total = ref(0);

  const loading = ref(false);

  const load = async () => {
    loading.value = true;
    try {
      const { data } = await getStockList(form.value);
      const { total: _total, list: _list } = data;

      total.value = _total;
      list.value = _list;

      if (!firstLoaded) {
        emit("onFirstLoaded", _list);
        firstLoaded = true;
      }
    } finally {
      loading.value = false;
    }
  };
  load();

  return {
    list,
    load,
    form,
    loading,
  };
};

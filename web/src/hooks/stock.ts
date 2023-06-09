import { ref } from "vue";
import { Stock } from "@/apis/typings";
import { getStockList } from "@/apis/stock";

export const useStockList = () => {
  const form = ref({
    page_current: 1,
    page_size: 100,
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

// 中文版內容包（LEDGER API）。由 Docker build ARG LANG 在建置時選擇，
// server.js 完全不判斷語言。狀態文字跟 FRONTIER 的 index.php 保持一致用詞。
module.exports = {
  cases: {
    1: { id: 1, name: "Eli Okafor", colony: "Eridanus II", status: "結案 - 死亡（醫療原因，6 歲）",
         case_ref: "OCPA-R4-11902", transfer_ref: "SPINDLE-7-0119" },
    2: { id: 2, name: "Talia Wren", colony: "Madrigal", status: "結案 - 死亡（醫療原因，6 歲）",
         case_ref: "OCPA-R4-11944", transfer_ref: "SPINDLE-7-0142" },
    3: { id: 3, name: "Dominic Farrow", colony: "Skopje", status: "結案 - 死亡（醫療原因，6 歲）",
         case_ref: "OCPA-R4-11887", transfer_ref: "SPINDLE-7-0087" },
    4: { id: 4, name: "Priya Anand", colony: "Eridanus II", status: "在案 - 一般被扶養人案件",
         case_ref: "OCPA-R4-12210", transfer_ref: null },
    5: { id: 5, type: "system", service: "ledger-cairn-sync", api_key: "sk-relay-7f2a9c1e4b8d3f6a",
         internal_notes: "LEDGER 案件索引與 CAIRN 長期檔案庫之間的每夜自動同步作業。不要停用 - 有法務保留（legal hold）中。" },
  },
  str: {
    case_not_found: "查無此案件",
    api_name: "LEDGER 案件索引 API",
  },
};

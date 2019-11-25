import { CompositeFilterDescriptor, FilterDescriptor, SortDescriptor } from '@progress/kendo-data-query';
import { Dictionary } from './dictionary';
import {
    FilterableSettings,
    GridDataResult,
    PageChangeEvent,
    PagerSettings,
    ScrollMode,
    SelectableSettings,
    SortSettings
    } from '@progress/kendo-angular-grid';
export class KendoGridSetting {
    data: GridDataResult;
    height: number;
    sort: SortDescriptor[] = [];
    pageSize: number;
    skip: number;
    filter: CompositeFilterDescriptor = {
        logic: 'and',
        filters: []
    };
    pageable: PagerSettings;
    sortable: SortSettings;
    selectable: SelectableSettings;
    scrollable: ScrollMode;
    resizable: boolean;
    filterable: FilterableSettings;
    sortFieldMapping: Dictionary<string> = {};
    constructor() {
        this.data = {
            data: [],
            total: 0
        } as GridDataResult;
        this.pageSize = 10;
        this.skip = 0;
        this.pageable = {
            buttonCount: 5,
            info: true,
            type: 'numeric',
            pageSizes: [20, 40, 60],
            previousNext: true
        };
        this.sortable = {
            allowUnsort: false,
            mode: 'single'
        };
        this.filter = {
            logic: 'and',
            filters: []
        } as CompositeFilterDescriptor;
        this.selectable = {
            enabled: true
        } as SelectableSettings;
        this.scrollable = 'scrollable';
        this.resizable = true;
        this.filterable = false;
    }
    public setPaging(e: PageChangeEvent) {
        this.skip = e.skip;
        this.pageSize = e.take;
    }
    public setSorting(sort: SortDescriptor[]) {
        this.sort = sort;
    }
    public setFilter(filter: CompositeFilterDescriptor) {
        this.filter = filter;
    }
}

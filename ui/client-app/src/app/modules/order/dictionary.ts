export interface Dictionary<T> {
    /**
     * Use string for key, and T for value.
     */
    [key: string]: T;
    [key: number]: T;
}

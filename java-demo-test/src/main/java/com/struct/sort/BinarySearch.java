package com.struct.sort;

public class BinarySearch {

    public static void main(String[] args){
        int[] array = {0,1,2,3,4,5,6,7};
        int[] arrays = {-99,-98,1,3,4,11,15,17};
        int index = RecursiveFind(arrays,-98,0,7);
//    int indexs = IteratorFind(arrays,-999);
        System.out.println("index = "+index);
//    System.out.println("indexs = "+indexs);
    }
    /**
     * 递归实现
     */
    public static int RecursiveFind(int[] array,int target,int start,int end){
        int mid = (end+start)/2;
        if (start>end || 0>end){
            return -1;
        }
        if (target>array[mid]){
            return RecursiveFind(array,target,mid+1,end);
        }else if (target<array[mid]){
            return RecursiveFind(array,target,start,mid-1);
        }else if (target==array[mid]){
            return mid;
        }else {
            return -1;
        }
    }
    /**
     * 迭代实现
     */
    public static int IteratorFind(int[] array,int target){
        int left = 0;
        int right = array.length-1;
        // 迭代实现使用while循环
        while (left<=right){
            int mid = (right+left)/2;
            if (target>array[mid]){
                left = mid+1;
            }else if (target<array[mid]){
                right = mid-1;
            }else {
                return mid;
            }
        }
        return -1;
    }
}

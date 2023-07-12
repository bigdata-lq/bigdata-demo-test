package struct.array;

import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.util.Arrays;

/**
 * @description:
 * @author: liquan
 * @time: 2022/11/15 0015 下午 14:52
 */
@Slf4j
public class ArrayTest {


    /**
     * 二分查找
     * @param arrs 有序
     * @param target
     * @return
     */
    public int search(int[] arrs,  int target){
        if (target < arrs[0] || target > arrs[arrs.length -1 ]){
            return -1;
        }
        int left = 0 ;
        int right = arrs.length -1;
        while (left <= right){
            int mid = (right - left) /2;
            if(arrs[mid] == target){
                return mid;
            } else if(arrs[mid] > target){
                left = mid + 1 ;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }

    /**
     * 移除元数据 单指针
     * 时间复杂度：O(n^2)
     * 空间复杂度：O(1)
     * @param arrs
     * @param val
     * @return
     */
    public int[] removeElement1(int[] arrs , int val){
        int size = arrs.length;
        for(int i = 0 ; i < size ; i ++){
            if( arrs[i] == val ){
                for (int j = i + 1; j < size; j++) {
                    arrs[j - 1] = arrs[j];
                }
                size --;  //需要将指针后移一位，因为此时i的位置上是原来i+1处的元
                i--; //因为删除了一个元素所以需要len--
            }
        }

        return Arrays.copyOf(arrs, size);
    }

    /**
     * 移除元数据 双指针
     * 时间复杂度：O(n)
     * 空间复杂度：O(1)
     * @param arrs
     * @param val
     * @return
     */
    public int[] removeElement2(int[] arrs , int val){
        int size  =  arrs.length;
        // 快慢指针
        int slowIndex = 0;
        for (int fastIndex = 0; fastIndex < arrs.length; fastIndex++) {
            if (arrs[fastIndex] != val ) {
                arrs[slowIndex] = arrs[fastIndex];
                slowIndex++;
            } else {
                size --;
            }
        }
        return Arrays.copyOf(arrs, size);
    }

    @Test
    public void removeElementTest(){
       int[] arrs1 = new int[] { 1, 2, 4, 2 ,19,20} ;
       log.info("单项指针删除元数以后的结果为：{}", removeElement1(arrs1, 2));
        int[] arrs2 = new int[] { 1, 2, 4, 2 ,19,20} ;
       log.info("快慢指针删除元数后的结果为{}", removeElement2(arrs2, 2));
    }

    @Test
    public void searchTest(){
        int[] arrs = new int[] { 1, 2, 4, 5 ,19,20} ;
        log.info("二分查找的结果：{}", search(arrs, 50));
        log.info("二分查找的结果：{}", search(arrs, 2));
        log.info("二分查找的结果：{}", search(arrs, -3));
    }
}

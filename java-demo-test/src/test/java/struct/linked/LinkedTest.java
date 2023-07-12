package struct.linked;

import com.struct.linked.OneLinkedList;
import com.struct.linked.TwoLinkedList;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

/**
 * @description:
 * @author: liquan
 * @time: 2022/11/16 0016 下午 16:09
 */
@Slf4j
public class LinkedTest {

    @Test
    public void testTwoLinkedList(){
        final TwoLinkedList twoLinkedList = new TwoLinkedList();
        twoLinkedList.addAtHead(1);
        for(int i = 1 ; i < 6 ; i ++){
            twoLinkedList.addAtIndex(i, i*i);
        }

        log.info("双链表添加数据数据：{}", twoLinkedList);

    }


    @Test
    public void testOneLinkedList(){
        final OneLinkedList oneLinkedList = new OneLinkedList();
        oneLinkedList.addAtHead(1);
        for(int i = 1 ; i < 6 ; i ++){
            oneLinkedList.addAtIndex(i, i*i);
        }

        log.info("单向链表添加数据数据：{}", oneLinkedList);

    }

}

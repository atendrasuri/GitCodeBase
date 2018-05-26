
import java.io.*;

class PrintThreeNumberSingleThread
  {
     public static void main(String args[])throws Exception
	  {
	  
	     PrintNumber obj= new PrintNumber();
		 
		 NumberThread one= new NumberThread(1, obj);
		  NumberThread two= new NumberThread(2, obj);
		   NumberThread three= new NumberThread(3, obj);
		   
		   Thread t1 = new Thread(one);
		   Thread t2 = new Thread(two);
		   Thread t3 = new Thread(three);
		   
		   t1.setName("one");
		   t2.setName("two");
		   t3.setName("three");
		   
		   t1.start();
		   t2.start();
		   t3.start();
		   
		   
		 
		 
	  }
  
  
  }
  
  class PrintNumber
    {
	    //boolean isOne=true;
		//boolean isTwo= false;
		//boolean isThree=false;
		int noflag=1;
	   PrintNumber(){
	   
	   }
	   
	   public void printOne()
	      {
		   for(int i=1;i<=30;i=i+3)
			   {
			     
				 synchronized(this)
			     {
			       //while(isOne==false)
				   while(noflag!=1)
				     {
					   try{
					   wait();
					    }catch(Exception e){}
					 }
					 try{
					   Thread.sleep(1000);
					    }catch(Exception e){}
						System.out.println(Thread.currentThread().getName()+""+i);
						//isOne=false;
						//isTwo=true;
						//isThree=false;
						noflag=2;
						notifyAll();
					 
			      }
			   
			 }  
		    
		  
		  
		  }
		  
		  public void printTwo(){
		       for(int i=2;i<=30;i=i+3)
			   {
			     
				 synchronized(this)
			     {
			       //while(isTwo==false)
				    while(noflag!=2)
				     {
					   try{
					   wait();
					    }catch(Exception e){}
					 }
					 try{
					   Thread.sleep(1000);
					    }catch(Exception e){}
						System.out.println(Thread.currentThread().getName()+""+i);
						//isOne=false;
						//isTwo=false;
						//isThree=true;
						noflag=3;
						notifyAll();
					 
			      }
			   
			 }  
		    
		  
		  }
		  
		  public void printThree()
		    {
			   for(int i=3;i<=30;i=i+3)
			   {
			     
				 synchronized(this)
			     {
			      // while(isThree==false)
				   while(noflag!=3)
				     {
					   try{
					   wait();
					    }catch(Exception e){}
					 }
					 try{
					   Thread.sleep(1000);
					    }catch(Exception e){}
						System.out.println(Thread.currentThread().getName()+""+i);
						//isOne=true;
						//isTwo=false;
						//isThree=false;
						noflag=1;
						notifyAll();
					 
			      }
			   
			 }  
		    
			
			}
		}
		
class NumberThread implements Runnable
    {
	
	    int no;
		PrintNumber obj;
		
	   NumberThread(int no, PrintNumber obj)
	     {
		    this.no=no;
			this.obj=obj;
		 
		 
		 }
		 
		 public void run(){
		 
		 
		         if(no==1)
				  {
				  
				     obj.printOne();
				  
				  }
				  if(no==2)
				  {
				  
				     obj.printTwo();
				  
				  }
				  if(no==3)
				  {
				  
				     obj.printThree();
				  
				  }
		 
		 
		 }
	
	
	}		